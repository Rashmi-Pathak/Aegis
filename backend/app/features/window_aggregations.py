"""AEGIS Rolling Window Statistical Feature Extraction
Extracts multi-scale moving statistics: mean, standard deviation, skewness, kurtosis, and quantile ratios.
"""

from typing import List, Dict, Any, Union
import numpy as np
import pandas as pd


class WindowAggregator:
    """Computes expanding and rolling statistical moments over time-ordered series."""

    @staticmethod
    def extract_rolling_features(
        series: pd.Series,
        windows: List[int] = [3, 7, 14, 30],
    ) -> pd.DataFrame:
        """Generates statistical summary moments across multiple temporal horizons."""
        s = pd.Series(series).astype(float)
        df = pd.DataFrame()

        for w in windows:
            rolled = s.rolling(window=w, min_periods=1)
            mean = rolled.mean()
            std = rolled.std().fillna(0.0)

            df[f"roll_mean_{w}"] = round(mean, 3)
            df[f"roll_std_{w}"] = round(std, 3)
            df[f"roll_min_{w}"] = round(rolled.min(), 3)
            df[f"roll_max_{w}"] = round(rolled.max(), 3)
            df[f"roll_z_ratio_{w}"] = round((s - mean) / (std + 1e-4), 3)

        # Exponentially weighted moving moments
        df["ewma_7"] = round(s.ewm(span=7).mean(), 3)
        df["ewma_28"] = round(s.ewm(span=28).mean(), 3)
        df["macd_spread"] = round(df["ewma_7"] - df["ewma_28"], 3)

        return df
