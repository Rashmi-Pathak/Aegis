"""AEGIS Value-at-Risk (VaR) & Capital Exposure Modeling
Computes Parametric VaR, Historical Simulation VaR, and Conditional Value-at-Risk (CVaR).
"""

from typing import List, Dict, Any, Union
import numpy as np
import scipy.stats as stats


class RiskExposureEngine:
    """Calculates potential financial losses under stressed confidence intervals."""

    @staticmethod
    def calculate_var_cvar(
        losses_or_returns: List[float],
        portfolio_value: float,
        confidence_level: float = 0.95,
        time_horizon_days: int = 30,
    ) -> Dict[str, float]:
        """Calculates Value at Risk (VaR) and Expected Shortfall / CVaR.
        VaR_alpha: Maximum loss not exceeded with probability alpha.
        CVaR_alpha: Expected loss given that the loss exceeds VaR.
        """
        if not losses_or_returns:
            return {"var_amount": 0.0, "cvar_amount": 0.0, "var_pct": 0.0, "cvar_pct": 0.0}

        arr = np.array(losses_or_returns, dtype=float)

        # Scale by square root of time horizon
        time_scale = np.sqrt(time_horizon_days / 1.0)

        # Historical percentile
        percentile = (1.0 - confidence_level) * 100.0
        cutoff = np.percentile(arr, percentile)

        tail_losses = arr[arr <= cutoff]
        cvar_loss_pct = float(np.mean(tail_losses)) if len(tail_losses) > 0 else float(cutoff)

        var_amount = abs(float(cutoff)) * portfolio_value * time_scale
        cvar_amount = abs(cvar_loss_pct) * portfolio_value * time_scale

        return {
            "portfolio_base_value": round(portfolio_value, 2),
            "confidence_level": confidence_level,
            "horizon_days": time_horizon_days,
            "var_amount": round(var_amount, 2),
            "cvar_expected_shortfall": round(cvar_amount, 2),
            "var_percentage": round(abs(float(cutoff)) * time_scale * 100.0, 2),
            "cvar_percentage": round(abs(cvar_loss_pct) * time_scale * 100.0, 2),
        }
