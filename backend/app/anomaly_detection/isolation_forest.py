"""AEGIS Multidimensional Isolation Forest Anomaly Detection
Uses tree ensemble space partitioning to detect multivariate structural outliers
in multidimensional enterprise telemetry.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


class IsolationForestDetector:
    """Multivariate anomaly detection wrapper around Scikit-Learn IsolationForest."""

    def __init__(
        self,
        contamination: float = 0.05,
        n_estimators: int = 150,
        random_state: int = 42,
    ):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
        )

    def fit_predict(
        self,
        features: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Fits isolation forest and returns outlier mask and normalized anomaly scores."""
        if features.empty:
            return {"is_anomaly": [], "anomaly_scores": []}

        # Impute numeric medians for safety
        clean_df = features.select_dtypes(include=[np.number]).fillna(features.median(numeric_only=True))

        if clean_df.empty or len(clean_df) < 5:
            return {
                "is_anomaly": [False] * len(features),
                "anomaly_scores": [0.0] * len(features),
            }

        # Predict returns -1 for outlier, 1 for inlier
        predictions = self.model.fit_predict(clean_df)
        raw_scores = self.model.decision_function(clean_df)

        # Normalize score: lower decision function means higher outlier probability
        min_s, max_s = raw_scores.min(), raw_scores.max()
        range_s = max_s - min_s if max_s != min_s else 1.0
        normalized_scores = 1.0 - ((raw_scores - min_s) / range_s)

        is_outlier = [bool(p == -1) for p in predictions]

        return {
            "is_anomaly": is_outlier,
            "anomaly_scores": [round(float(s), 4) for s in normalized_scores],
            "outlier_count": int(np.sum(is_outlier)),
            "contamination_rate": round(float(np.mean(is_outlier)), 4),
        }
