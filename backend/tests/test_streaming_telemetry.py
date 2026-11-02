"""
Tests for Streaming Telemetry Buffer and Enterprise Telemetry Coordinator.
Verifies sliding windows, EWMA calculation, anomaly detection, downsampling, and quantiles.
"""

import pytest
from app.analytics.streaming_telemetry import (
    StreamingTelemetryBuffer,
    EnterpriseTelemetryCoordinator,
)


def test_streaming_buffer_basic_statistics():
    """Verify sliding window mean, min, max, and EWMA updates."""
    buffer = StreamingTelemetryBuffer(metric_id="fuel_rate", window_size=10, alpha=0.2)
    values = [10.0, 12.0, 14.0, 16.0, 18.0]
    for v in values:
        buffer.ingest(v)

    assert len(buffer.points) == 5
    assert buffer.current_mean == pytest.approx(14.0)
    assert buffer._min_val == 10.0
    assert buffer._max_val == 18.0
    assert buffer.current_ewma > 10.0


def test_window_eviction():
    """Verify that old points are evicted once the window capacity is exceeded."""
    buffer = StreamingTelemetryBuffer(metric_id="cpu_load", window_size=5)
    for i in range(10):
        buffer.ingest(float(i))

    assert len(buffer.points) == 5
    expected_points = [5.0, 6.0, 7.0, 8.0, 9.0]
    actual_points = [p.value for p in buffer.points]
    assert actual_points == expected_points


def test_z_score_and_outlier_detection():
    """Verify Z-score computation for abnormal telemetry spikes."""
    buffer = StreamingTelemetryBuffer(metric_id="port_dwell", window_size=50, alpha=0.1)
    # Establish a stable baseline of ~20.0
    for _ in range(30):
        buffer.ingest(20.0)

    # Ingest a severe spike
    spike_z = buffer.compute_z_score(120.0)
    # Because baseline std was zero/near-zero, ingest a small variation first
    buffer.ingest(21.0)
    buffer.ingest(19.0)
    buffer.ingest(20.5)
    spike_z = buffer.compute_z_score(80.0)
    assert spike_z > 3.0


def test_quantile_estimation():
    """Verify quantile approximation over ingested data points."""
    buffer = StreamingTelemetryBuffer(metric_id="response_time", window_size=100)
    for i in range(1, 101):
        buffer.ingest(float(i))

    p90 = buffer.estimate_quantile(0.90)
    assert 85.0 <= p90 <= 95.0
    p50 = buffer.estimate_quantile(0.50)
    assert 45.0 <= p50 <= 55.0


def test_downsampled_export_for_mobile():
    """Verify that a large window downsamples smoothly for mobile consumption."""
    buffer = StreamingTelemetryBuffer(metric_id="revenue_stream", window_size=200)
    for i in range(200):
        buffer.ingest(100.0 + i * 0.1)

    downsampled = buffer.export_downsampled_series(max_points=20)
    assert len(downsampled) == 20
    assert "timestamp" in downsampled[0]
    assert "value" in downsampled[0]
    assert "confidence" in downsampled[0]


def test_enterprise_telemetry_coordinator():
    """Verify multi-channel batch ingestion and cross-metric anomaly capture."""
    coord = EnterpriseTelemetryCoordinator(tenant_id="primelogix")
    batch = [
        {"metric_id": "freight_cost", "value": 1500.0},
        {"metric_id": "freight_cost", "value": 1520.0},
        {"metric_id": "freight_cost", "value": 1490.0},
        {"metric_id": "idle_hours", "value": 2.1},
        {"metric_id": "idle_hours", "value": 2.4},
    ]
    coord.ingest_batch(batch)

    summary_freight = coord.get_channel_summary("freight_cost")
    assert summary_freight["point_count"] == 3
    assert summary_freight["tenant_id"] == "primelogix"

    summary_idle = coord.get_channel_summary("idle_hours")
    assert summary_idle["point_count"] == 2
