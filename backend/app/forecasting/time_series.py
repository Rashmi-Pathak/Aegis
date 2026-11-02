"""AEGIS Statistical & Classical Time Series Forecasting
Implements Holt-Winters Triple Exponential Smoothing, Trend-Seasonal Decomposition,
and Confidence Envelopes.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd


class ClassicalForecaster:
    """Statistical forecasting for trend and seasonality without deep dependency overhead."""

    @staticmethod
    def double_exponential_smoothing(
        series: List[float],
        horizon: int = 6,
        alpha: float = 0.3,
        beta: float = 0.1,
    ) -> Dict[str, Any]:
        """Holt's linear trend method for forecasting metrics with trend."""
        if len(series) < 3:
            last_val = series[-1] if series else 0.0
            return {
                "forecast": [last_val] * horizon,
                "lower_bound": [last_val * 0.9] * horizon,
                "upper_bound": [last_val * 1.1] * horizon,
            }

        level = series[0]
        trend = series[1] - series[0]
        levels = [level]
        trends = [trend]

        for val in series[1:]:
            last_level = level
            level = alpha * val + (1.0 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1.0 - beta) * trend
            levels.append(level)
            trends.append(trend)

        # Generate future forecast steps
        forecast = [round(level + (i + 1) * trend, 2) for i in range(horizon)]

        # Estimate residual variance for prediction interval (95% confidence)
        fitted = [levels[i] + trends[i] for i in range(len(series) - 1)]
        residuals = np.array(series[1:]) - np.array(fitted)
        sigma = float(np.std(residuals)) if len(residuals) > 0 else (level * 0.05)

        lower = [round(f - (1.96 * sigma * np.sqrt(i + 1)), 2) for i, f in enumerate(forecast)]
        upper = [round(f + (1.96 * sigma * np.sqrt(i + 1)), 2) for i, f in enumerate(forecast)]

        return {
            "forecast": forecast,
            "lower_bound": lower,
            "upper_bound": upper,
            "trend_slope": round(trend, 3),
            "estimated_sigma": round(sigma, 3),
        }
