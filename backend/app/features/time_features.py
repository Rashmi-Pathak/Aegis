"""AEGIS Time & Calendar Feature Engineering
Extracts cyclical calendar representations and seasonal indicators from timestamps.
"""

from typing import List, Dict, Any, Union
import numpy as np
import pandas as pd


class TimeFeatureEngineer:
    """Generates cyclical sine/cosine encodings, holiday flags, and business day markers."""

    @staticmethod
    def extract_cyclical_features(timestamps: Union[List[str], pd.Series]) -> pd.DataFrame:
        """Transforms timestamps into continuous cyclical features for gradient boosting and linear models."""
        dt = pd.to_datetime(timestamps, errors="coerce")

        df = pd.DataFrame()
        # Day of week cyclical (0-6)
        day_of_week = dt.dt.dayofweek
        df["dow_sin"] = np.sin(2.0 * np.pi * day_of_week / 7.0)
        df["dow_cos"] = np.cos(2.0 * np.pi * day_of_week / 7.0)

        # Month cyclical (1-12)
        month = dt.dt.month
        df["month_sin"] = np.sin(2.0 * np.pi * (month - 1) / 12.0)
        df["month_cos"] = np.cos(2.0 * np.pi * (month - 1) / 12.0)

        # Day of year cyclical
        doy = dt.dt.dayofyear
        df["doy_sin"] = np.sin(2.0 * np.pi * doy / 365.25)
        df["doy_cos"] = np.cos(2.0 * np.pi * doy / 365.25)

        # Flags
        df["is_weekend"] = day_of_week.isin([5, 6]).astype(int)
        df["is_quarter_end"] = dt.dt.is_quarter_end.astype(int)
        df["is_month_end"] = dt.dt.is_month_end.astype(int)

        return df
