"""AEGIS Local Outlier Factor (LOF) Density-Based Anomaly Detection
Detects points with substantially lower density than their k-nearest neighbors,
ideal for catching localized operational anomalies in clustered enterprise telemetry.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor


class LOFDetector:
    """Density-based anomaly detector measuring local deviation with respect to neighbors."""

    def __init__(self, n_neighbors: int = 20, contamination: float = 0.05):
        self.n_neighbors = n_neighbors
        self.contamination = contamination

    def fit_predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Runs LOF on numerical features and produces anomaly indicators."""
        if features.empty:
            return {"is_anomaly": [], "anomaly_scores": []}

        clean_df = features.select_dtypes(include=[np.number]).fillna(0.0)

        n_samples = len(clean_df)
        if n_samples < 10:
            return {
                "is_anomaly": [False] * n_samples,
                "anomaly_scores": [0.0] * n_samples,
            }

        k = min(self.n_neighbors, max(2, n_samples // 3))
        lof = LocalOutlierFactor(n_neighbors=k, contamination=self.contamination)

        pred = lof.fit_predict(clean_df)
        factors = -lof.negative_outlier_factor_

        # Scores > 1.5 usually denote strong localized isolation
        min_f, max_f = factors.min(), factors.max()
        range_f = max_f - min_f if max_f != min_f else 1.0
        normalized_scores = (factors - min_f) / range_f

        is_outlier = [bool(p == -1) for p in pred]

        return {
            "is_anomaly": is_outlier,
            "anomaly_scores": [round(float(s), 4) for s in normalized_scores],
            "raw_lof_factors": [round(float(f), 3) for f in factors],
            "outlier_count": int(np.sum(is_outlier)),
        }
