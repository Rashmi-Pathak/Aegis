"""AEGIS Time Series Anomaly Engine
Implements Rolling Bollinger Bands, Seasonal ESD (Extreme Studentized Deviate),
and Exponentially Weighted Moving Average (EWMA) deviation tracking.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


class TimeSeriesAnomalyDetector:
    """Detects temporal spikes, structural level shifts, and variance drift in time series."""

    @staticmethod
    def rolling_bollinger_bands(
        series: pd.Series,
        window: int = 7,
        num_std: float = 2.5,
    ) -> Dict[str, Any]:
        """Calculates dynamic upper and lower Bollinger envelopes and flags breaches."""
        s = pd.Series(series).astype(float)
        # Shift by 1 so the current observation does not inflate its own mean/std window
        shifted = s.shift(1)
        rolling_mean = shifted.rolling(window=window, min_periods=2).mean().bfill()
        rolling_std = shifted.rolling(window=window, min_periods=2).std().bfill()

        # Fallback for initial flat lines
        rolling_std = rolling_std.replace(0.0, float(s.std()) if float(s.std()) > 0 else 1.0)

        upper_band = rolling_mean + (num_std * rolling_std)
        lower_band = rolling_mean - (num_std * rolling_std)

        breach_upper = s > upper_band
        breach_lower = s < lower_band
        is_anomaly = breach_upper | breach_lower

        return {
            "is_anomaly": is_anomaly.tolist(),
            "upper_band": [round(float(x), 2) for x in upper_band],
            "lower_band": [round(float(x), 2) for x in lower_band],
            "rolling_mean": [round(float(x), 2) for x in rolling_mean],
            "anomaly_indices": [int(i) for i in np.where(is_anomaly)[0]],
            "outlier_count": int(is_anomaly.sum()),
        }

    @staticmethod
    def ewma_residual_detector(
        series: pd.Series,
        span: int = 14,
        threshold_multiplier: float = 3.0,
    ) -> Dict[str, Any]:
        """Flags large residuals between actual values and exponentially weighted forecasts."""
        s = pd.Series(series).astype(float)
        ewma = s.ewm(span=span, adjust=False).mean()
        residual = s - ewma
        residual_std = residual.std()

        if residual_std == 0:
            return {"is_anomaly": [False] * len(s), "residuals": [0.0] * len(s)}

        z_res = (residual / residual_std).abs()
        is_anomaly = z_res > threshold_multiplier

        return {
            "is_anomaly": is_anomaly.tolist(),
            "ewma_baseline": [round(float(x), 2) for x in ewma],
            "residuals": [round(float(x), 2) for x in residual],
            "outlier_count": int(is_anomaly.sum()),
        }
