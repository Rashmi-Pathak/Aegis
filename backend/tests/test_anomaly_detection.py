import pytest
import pandas as pd
import numpy as np
from app.anomaly_detection.isolation_forest import IsolationForestDetector
from app.anomaly_detection.local_outlier_factor import LOFDetector
from app.anomaly_detection.statistical_anomaly import StatisticalAnomalyDetector
from app.anomaly_detection.time_series_anomaly import TimeSeriesAnomalyDetector
from app.anomaly_detection.anomaly_engine import AnomalyDetectionEngine

def test_statistical_z_score():
    data = [10.0, 10.2, 9.8, 10.1, 9.9, 100.0]  # 100.0 is an extreme outlier
    res = StatisticalAnomalyDetector.z_score_detector(data, threshold=2.0)
    assert res["outlier_count"] >= 1
    assert res["is_anomaly"][-1] is True

def test_modified_z_score_mad():
    data = [10.0, 10.2, 9.8, 10.1, 9.9, 10.0, 95.0]
    res = StatisticalAnomalyDetector.modified_z_score_mad(data, threshold=3.0)
    assert res["outlier_count"] >= 1
    assert res["is_anomaly"][-1] is True

def test_time_series_bollinger():
    series = [10, 10, 10, 11, 10, 10, 10, 50, 10, 10]
    res = TimeSeriesAnomalyDetector.rolling_bollinger_bands(series, window=4, num_std=2.0)
    assert res["outlier_count"] >= 1
    assert 7 in res["anomaly_indices"]

def test_isolation_forest():
    np.random.seed(42)
    normal = np.random.normal(loc=10.0, scale=1.0, size=(100, 2))
    outliers = np.array([[50.0, 50.0], [60.0, 60.0]])
    data = np.vstack([normal, outliers])
    df = pd.DataFrame(data, columns=["feature1", "feature2"])

    detector = IsolationForestDetector(contamination=0.03)
    res = detector.fit_predict(df)
    assert res["outlier_count"] >= 1
    assert res["is_anomaly"][-1] is True

def test_anomaly_engine():
    np.random.seed(42)
    df = pd.DataFrame({
        "revenue": list(np.random.normal(100, 5, 50)) + [500.0],
        "costs": list(np.random.normal(80, 4, 50)) + [400.0],
    })
    res = AnomalyDetectionEngine.analyze_dataset(df, contamination=0.05)
    assert res["anomalies_detected"] >= 1
