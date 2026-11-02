"""AEGIS Quantile Regression & Asymmetric Loss Forecasting
Optimizes pinball / check loss to construct non-parametric prediction bounds (P10, P50, P90).
"""

from typing import List, Dict, Any
import numpy as np


class QuantileLossForecaster:
    """Computes asymmetric quantile loss bounds for conservative capital reserve planning."""

    @staticmethod
    def pinball_loss(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        quantile: float,
    ) -> float:
        """L_q(y, y_hat) = max(q * (y - y_hat), (1 - q) * (y_hat - y))"""
        diff = y_true - y_pred
        loss = np.maximum(quantile * diff, (quantile - 1.0) * diff)
        return float(np.mean(loss))

    @classmethod
    def estimate_asymmetric_intervals(
        cls,
        point_forecast: List[float],
        historical_residuals: List[float],
        quantiles: List[float] = [0.10, 0.50, 0.90],
    ) -> Dict[str, List[float]]:
        """Maps historical empirical quantile offsets directly onto point predictions."""
        res_arr = np.array(historical_residuals)
        offsets = {q: float(np.percentile(res_arr, q * 100.0)) for q in quantiles}

        result = {}
        for q, offset in offsets.items():
            key = f"P{int(q * 100)}"
            result[key] = [round(val + offset, 2) for val in point_forecast]

        return result
