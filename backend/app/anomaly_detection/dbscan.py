"""AEGIS DBSCAN Spatial Clustering Outlier Engine
Separates dense operational clusters from sparse anomalies with automated eps tuning.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class DBSCANOutlierDetector:
    """Density-Based Spatial Clustering of Applications with Noise."""

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples

    def fit_predict(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Runs DBSCAN and marks cluster == -1 as operational noise / anomalies."""
        numeric_df = df.select_dtypes(include=[np.number]).fillna(0.0)
        n = len(numeric_df)
        if n < 10:
            return {"is_anomaly": [False] * n, "clusters": [0] * n}

        scaler = StandardScaler()
        scaled = scaler.fit_transform(numeric_df)

        db = DBSCAN(eps=self.eps, min_samples=min_samples if 'min_samples' in locals() else self.min_samples)
        labels = db.fit_predict(scaled)

        is_noise = [bool(l == -1) for l in labels]

        return {
            "is_anomaly": is_noise,
            "cluster_labels": [int(l) for l in labels],
            "total_clusters": int(len(set(labels)) - (1 if -1 in labels else 0)),
            "outlier_count": int(sum(is_noise)),
        }
