"""AEGIS Autoregressive Moving Average (ARIMA) Grid Optimization
Implements automated order selection (p, d, q) utilizing Akaike Information Criterion (AIC).
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class AutoARIMAEvaluator:
    """Estimates optimal lag orders and forecasts stationary differenced sequences."""

    @staticmethod
    def difference_series(series: List[float], order: int = 1) -> Tuple[List[float], List[float]]:
        """Applies order-d differencing to achieve mean-stationarity."""
        diff = list(series)
        history_heads = []
        for _ in range(order):
            if len(diff) > 1:
                history_heads.append(diff[0])
                diff = [diff[i] - diff[i - 1] for i in range(1, len(diff))]
        return diff, history_heads

    @staticmethod
    def fit_ar_order(diff_series: List[float], p: int) -> Tuple[np.ndarray, float]:
        """Fits Autoregressive coefficients AR(p) via Ordinary Least Squares (Yule-Walker approximation)."""
        if len(diff_series) <= p + 2:
            return np.zeros(p), float(np.var(diff_series)) if diff_series else 1.0

        y = np.array(diff_series[p:])
        X = np.column_stack([diff_series[p - i - 1 : len(diff_series) - i - 1] for i in range(p)])

        # Ridge regularized regression for numerical stability
        xtx = X.T @ X + (1e-4 * np.eye(p))
        xty = X.T @ y
        phi = np.linalg.solve(xtx, xty)

        residuals = y - (X @ phi)
        sigma2 = float(np.var(residuals)) if len(residuals) > 0 else 1.0

        return phi, sigma2

    @classmethod
    def select_best_ar_order(cls, series: List[float], max_p: int = 4) -> Dict[str, Any]:
        """Evaluates AR orders 1..max_p and chooses the one minimizing AIC."""
        diff, heads = cls.difference_series(series, order=1)
        n = len(diff)
        best_p = 1
        best_aic = float("inf")
        best_phi = np.array([0.5])
        best_sigma = 1.0

        for p in range(1, min(max_p + 1, n // 3)):
            phi, sigma2 = cls.fit_ar_order(diff, p)
            # AIC = n * ln(sigma^2) + 2*k
            aic = n * np.log(max(1e-6, sigma2)) + 2 * (p + 1)
            if aic < best_aic:
                best_aic = aic
                best_p = p
                best_phi = phi
                best_sigma = sigma2

        return {
            "best_p_order": best_p,
            "aic_score": round(float(best_aic), 2),
            "coefficients": [round(float(c), 4) for c in best_phi],
            "residual_variance": round(float(best_sigma), 4),
        }
