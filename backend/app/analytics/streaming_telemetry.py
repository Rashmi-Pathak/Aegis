"""
AEGIS — Streaming Telemetry & Low-Latency Window Buffer.
Processes high-frequency IoT, ERP, and transactional business events with sliding quantile estimators,
exponential variance smoothers, and adaptive edge compression for mobile and desktop clients.
"""

import math
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class TelemetryDataPoint:
    """Represents a timestamped scalar telemetry observation."""
    metric_id: str
    value: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: Dict[str, str] = field(default_factory=dict)
    confidence: float = 1.0


class StreamingTelemetryBuffer:
    """Sliding window buffer for streaming business telemetry with EWMA and quantile tracking."""

    def __init__(
        self,
        metric_id: str,
        window_size: int = 500,
        alpha: float = 0.15,
        target_quantile: float = 0.95,
    ):
        self.metric_id = metric_id
        self.window_size = window_size
        self.alpha = alpha
        self.target_quantile = target_quantile
        self.points: List[TelemetryDataPoint] = []
        self._ewma: Optional[float] = None
        self._ewmv: Optional[float] = None  # Exponentially weighted moving variance
        self._min_val: float = float("inf")
        self._max_val: float = float("-inf")
        self._sum: float = 0.0
        self._count: int = 0

    def ingest(self, value: float, tags: Optional[Dict[str, str]] = None, confidence: float = 1.0) -> None:
        """Ingests a new metric measurement into the sliding window and updates running statistics."""
        point = TelemetryDataPoint(
            metric_id=self.metric_id,
            value=value,
            tags=tags or {},
            confidence=confidence,
        )
        self.points.append(point)
        self._count += 1
        self._sum += value
        if value < self._min_val:
            self._min_val = value
        if value > self._max_val:
            self._max_val = value

        # Update EWMA
        if self._ewma is None:
            self._ewma = value
            self._ewmv = 0.0
        else:
            delta = value - self._ewma
            self._ewma += self.alpha * delta
            # Incremental variance update
            self._ewmv = (1.0 - self.alpha) * (self._ewmv + self.alpha * (delta ** 2))

        # Evict oldest points when capacity exceeded
        if len(self.points) > self.window_size:
            evicted = self.points.pop(0)
            self._sum -= evicted.value

    @property
    def current_mean(self) -> float:
        """Computes current sliding window mean."""
        if not self.points:
            return 0.0
        return self._sum / len(self.points)

    @property
    def current_ewma(self) -> float:
        """Returns the exponentially weighted moving average."""
        return self._ewma if self._ewma is not None else 0.0

    @property
    def current_std(self) -> float:
        """Returns standard deviation of sliding window."""
        if self._ewmv is not None and self._ewmv > 0:
            return math.sqrt(self._ewmv)
        if len(self.points) < 2:
            return 0.0
        mean = self.current_mean
        variance = sum((p.value - mean) ** 2 for p in self.points) / (len(self.points) - 1)
        return math.sqrt(max(0.0, variance))

    def compute_z_score(self, value: float) -> float:
        """Calculates standard score (Z-Score) relative to the active EWMA baseline."""
        std = self.current_std
        if std <= 1e-6:
            return 0.0
        return (value - self.current_ewma) / std

    def estimate_quantile(self, q: Optional[float] = None) -> float:
        """Estimates target percentile via sorted nearest-rank interpolation."""
        target = q if q is not None else self.target_quantile
        if not self.points:
            return 0.0
        sorted_vals = sorted(p.value for p in self.points)
        idx = max(0, min(len(sorted_vals) - 1, int(target * len(sorted_vals))))
        return sorted_vals[idx]

    def export_downsampled_series(self, max_points: int = 24) -> List[Dict[str, Any]]:
        """Downsamples the active window for high-performance mobile UI rendering without latency."""
        if not self.points:
            return []
        if len(self.points) <= max_points:
            return [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "value": round(p.value, 2),
                    "confidence": p.confidence,
                }
                for p in self.points
            ]

        step = len(self.points) / max_points
        sampled = []
        for i in range(max_points):
            idx = min(len(self.points) - 1, int(i * step))
            p = self.points[idx]
            sampled.append({
                "timestamp": p.timestamp.isoformat(),
                "value": round(p.value, 2),
                "confidence": p.confidence,
            })
        return sampled

    def clear(self) -> None:
        """Flushes the sliding window."""
        self.points.clear()
        self._ewma = None
        self._ewmv = None
        self._min_val = float("inf")
        self._max_val = float("-inf")
        self._sum = 0.0
        self._count = 0


class EnterpriseTelemetryCoordinator:
    """Coordinates multiple streaming metric channels for real-time risk evaluation."""

    def __init__(self, tenant_id: str = "primelogix"):
        self.tenant_id = tenant_id
        self.channels: Dict[str, StreamingTelemetryBuffer] = {}
        self.alert_triggers: List[Dict[str, Any]] = []

    def get_or_create_channel(self, metric_id: str, window_size: int = 500) -> StreamingTelemetryBuffer:
        """Retrieves or provisions a metric channel buffer."""
        if metric_id not in self.channels:
            self.channels[metric_id] = StreamingTelemetryBuffer(metric_id=metric_id, window_size=window_size)
        return self.channels[metric_id]

    def ingest_batch(self, measurements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ingests a telemetry batch and checks for anomalies across all channels."""
        anomalies_detected = []
        for m in measurements:
            metric_id = m["metric_id"]
            value = float(m["value"])
            channel = self.get_or_create_channel(metric_id)
            channel.ingest(value, tags=m.get("tags"), confidence=m.get("confidence", 1.0))

            z_score = channel.compute_z_score(value)
            if abs(z_score) >= 3.0:
                anomaly = {
                    "tenant_id": self.tenant_id,
                    "metric_id": metric_id,
                    "observed_value": value,
                    "baseline_ewma": round(channel.current_ewma, 2),
                    "z_score": round(z_score, 2),
                    "severity": "critical" if abs(z_score) >= 4.0 else "high",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                anomalies_detected.append(anomaly)
                self.alert_triggers.append(anomaly)

        return anomalies_detected

    def get_channel_summary(self, metric_id: str) -> Dict[str, Any]:
        """Returns consolidated statistical diagnostics for a metric channel."""
        channel = self.channels.get(metric_id)
        if not channel:
            return {"metric_id": metric_id, "status": "uninitialized"}
        return {
            "tenant_id": self.tenant_id,
            "metric_id": metric_id,
            "point_count": len(channel.points),
            "mean": round(channel.current_mean, 2),
            "ewma": round(channel.current_ewma, 2),
            "std_dev": round(channel.current_std, 2),
            "p95": round(channel.estimate_quantile(0.95), 2),
            "p99": round(channel.estimate_quantile(0.99), 2),
            "active_alerts": len([a for a in self.alert_triggers if a["metric_id"] == metric_id]),
        }
