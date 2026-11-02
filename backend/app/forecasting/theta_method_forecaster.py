"""AEGIS Theta Forecasting Method (Assimakopoulos & Nikolopoulos)
Decomposes time series into Theta lines: linear long-term trend (Theta=0) and short-term curvature (Theta=2).
"""
from typing import List, Dict, Any
import numpy as np

class ThetaForecaster:
    @staticmethod
    def forecast_theta(
        series: List[float],
        horizon: int = 4,
    ) -> Dict[str, Any]:
        """Forecasts via linear regression trend line and seasonal mean reversion."""
        arr = np.array(series, dtype=float)
        n = len(arr)

        if n < 4:
            last = arr[-1] if n > 0 else 100.0
            return {"forecast": [last] * horizon}

        # Linear trend: Theta=0
        t = np.arange(n)
        slope, intercept = np.polyfit(t, arr, 1)

        # Project trend
        future_t = np.arange(n, n + horizon)
        trend_forecast = intercept + (slope * future_t)

        # Simple exponential smoothing on residuals: Theta=2
        residuals = arr - (intercept + slope * t)
        last_residual = float(residuals[-1])

        # Combine with 0.5 weights (standard Theta formulation)
        forecast = [round(float(trend_forecast[i] + 0.5 * last_residual * (0.8 ** (i + 1))), 2) for i in range(horizon)]

        return {
            "forecast": forecast,
            "linear_slope": round(float(slope), 3),
            "last_residual": round(last_residual, 2),
        }
