"""AEGIS Univariate Statistical Anomaly Engine
Calculates parametric Z-scores, non-parametric Median Absolute Deviation (MAD),
and Tukey Interquartile Range (IQR) fences.
"""

from typing import List, Dict, Any, Union
import numpy as np
import pandas as pd


class StatisticalAnomalyDetector:
    """Statistical univariate anomaly detection for single metric streams."""

    @staticmethod
    def z_score_detector(
        values: Union[List[float], pd.Series],
        threshold: float = 3.0,
    ) -> Dict[str, Any]:
        """Detects points where |Z| > threshold."""
        arr = np.array(values, dtype=float)
        mean = np.nanmean(arr)
        std = np.nanstd(arr)

        if std == 0 or np.isnan(std):
            return {"is_anomaly": [False] * len(arr), "z_scores": [0.0] * len(arr)}

        z_scores = (arr - mean) / std
        is_anomaly = [bool(abs(z) > threshold) for z in z_scores]

        return {
            "is_anomaly": is_anomaly,
            "z_scores": [round(float(z), 3) if not np.isnan(z) else 0.0 for z in z_scores],
            "threshold": threshold,
            "outlier_count": int(sum(is_anomaly)),
        }

    @staticmethod
    def modified_z_score_mad(
        values: Union[List[float], pd.Series],
        threshold: float = 3.5,
    ) -> Dict[str, Any]:
        """Boris Iglewicz and David Hoaglin modified Z-score using Median Absolute Deviation.
        Robust against extreme maskings and skewed distributions.
        M_i = 0.6745 * (x_i - median) / MAD
        """
        arr = np.array(values, dtype=float)
        med = np.nanmedian(arr)
        mad = np.nanmedian(np.abs(arr - med))

        if mad == 0:
            return {"is_anomaly": [False] * len(arr), "modified_z_scores": [0.0] * len(arr)}

        modified_z = 0.6745 * (arr - med) / mad
        is_anomaly = [bool(abs(mz) > threshold) for mz in modified_z]

        return {
            "is_anomaly": is_anomaly,
            "modified_z_scores": [round(float(mz), 3) if not np.isnan(mz) else 0.0 for mz in modified_z],
            "threshold": threshold,
            "outlier_count": int(sum(is_anomaly)),
        }

    @staticmethod
    def iqr_fence_detector(
        values: Union[List[float], pd.Series],
        k: float = 1.5,
    ) -> Dict[str, Any]:
        """Tukey IQR Fences: [Q1 - k*IQR, Q3 + k*IQR]."""
        arr = np.array(values, dtype=float)
        q1 = np.nanpercentile(arr, 25)
        q3 = np.nanpercentile(arr, 75)
        iqr = q3 - q1

        lower_fence = q1 - (k * iqr)
        upper_fence = q3 + (k * iqr)

        is_anomaly = [bool(x < lower_fence or x > upper_fence) for x in arr]

        return {
            "is_anomaly": is_anomaly,
            "lower_bound": round(float(lower_fence), 3),
            "upper_bound": round(float(upper_fence), 3),
            "iqr": round(float(iqr), 3),
            "outlier_count": int(sum(is_anomaly)),
        }
