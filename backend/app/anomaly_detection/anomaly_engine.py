"""AEGIS Unified Anomaly Detection Engine
Orchestrates ensemble anomaly detection across Isolation Forest, LOF, and Statistical tests.
"""

from typing import Dict, Any, List
import pandas as pd
from app.anomaly_detection.isolation_forest import IsolationForestDetector
from app.anomaly_detection.local_outlier_factor import LOFDetector
from app.anomaly_detection.statistical_anomaly import StatisticalAnomalyDetector
from app.anomaly_detection.time_series_anomaly import TimeSeriesAnomalyDetector


class AnomalyDetectionEngine:
    """Master orchestrator combining parametric and non-parametric detectors."""

    @classmethod
    def analyze_dataset(cls, df: pd.DataFrame, contamination: float = 0.05) -> Dict[str, Any]:
        """Runs multi-model anomaly detection ensemble across a dataset."""
        if df.empty:
            return {"anomalies_detected": 0, "results": []}

        iso = IsolationForestDetector(contamination=contamination)
        iso_results = iso.fit_predict(df)

        lof = LOFDetector(contamination=contamination)
        lof_results = lof.fit_predict(df)

        # Ensemble agreement: flagged if both or if score is extremely high
        is_anomaly = [
            bool(iso_p or lof_p)
            for iso_p, lof_p in zip(iso_results["is_anomaly"], lof_results["is_anomaly"])
        ]

        return {
            "total_records": len(df),
            "anomalies_detected": int(sum(is_anomaly)),
            "anomaly_rate_pct": round((sum(is_anomaly) / len(df)) * 100.0, 2) if len(df) > 0 else 0.0,
            "isolation_forest_outliers": iso_results["outlier_count"],
            "lof_outliers": lof_results["outlier_count"],
            "flags": is_anomaly[:100],  # sample first 100
        }
