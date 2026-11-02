"""AEGIS Extreme Value Theory (EVT) & Tail Risk Engine
Fits Generalized Pareto Distribution (GPD) over high thresholds to model extreme fat-tailed Black Swan losses.
"""
from typing import Dict, Any, List
import numpy as np

class ExtremeValueTheoryEngine:
    @staticmethod
    def peaks_over_threshold_gpd(
        losses: List[float],
        threshold_quantile: float = 0.90,
    ) -> Dict[str, Any]:
        """Calculates GPD tail parameters (shape xi, scale beta) for losses exceeding threshold u."""
        arr = np.array(losses, dtype=float)
        u = float(np.percentile(arr, threshold_quantile * 100.0))
        exceedances = arr[arr > u] - u

        if len(exceedances) < 5:
            return {"threshold_u": u, "tail_shape_xi": 0.0, "status": "Insufficient Tail Sample"}

        # Method of Moments GPD estimator
        mean_excess = float(np.mean(exceedances))
        var_excess = float(np.var(exceedances))

        if var_excess > 0:
            xi = 0.5 * (1.0 - ((mean_excess ** 2) / var_excess))
            sigma = 0.5 * mean_excess * (((mean_excess ** 2) / var_excess) + 1.0)
        else:
            xi, sigma = 0.0, mean_excess

        # 99.9% 1-in-1000 year catastrophic Black Swan loss
        n_total = len(arr)
        n_exceed = len(exceedances)
        p_target = 0.999

        if xi != 0:
            black_swan_val = u + (sigma / xi) * ((((n_total / n_exceed) * (1.0 - p_target)) ** (-xi)) - 1.0)
        else:
            black_swan_val = u - sigma * np.log((n_total / n_exceed) * (1.0 - p_target))

        return {
            "threshold_u": round(u, 2),
            "tail_shape_parameter_xi": round(float(xi), 3),
            "tail_scale_parameter_sigma": round(float(sigma), 2),
            "black_swan_loss_p999_usd": round(float(black_swan_val), 2),
            "tail_classification": "Heavy Fat-Tailed (Fréchet Domain)" if xi > 0 else "Thin-Tailed (Gumbel)",
        }
