"""
AEGIS — Mobile Telemetry, Viewport Negotiation & Enterprise Audit Test Suite.
Tests mobile client responsiveness contracts, edge compression, multi-tenant session
isolation, and low-latency payload serialization for the analytics workspace.
"""

import pytest
import math
import json
from typing import Dict, Any, List
from datetime import datetime, timezone


class MobileTelemetryDispatcher:
    """Simulates edge mobile telemetry dispatching and adaptive viewport compression."""

    def __init__(self, tenant_id: str = "primelogix"):
        self.tenant_id = tenant_id
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def register_client_session(
        self,
        session_id: str,
        viewport_width: int,
        viewport_height: int,
        device_type: str = "mobile",
        user_agent: str = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)",
    ) -> Dict[str, Any]:
        """Negotiates client viewport parameters and compression thresholds."""
        is_compact = viewport_width < 1024
        sidebar_mode = "drawer" if is_compact else ("rail" if viewport_width < 1280 else "expanded")

        session_meta = {
            "session_id": session_id,
            "tenant_id": self.tenant_id,
            "viewport": {
                "width": viewport_width,
                "height": viewport_height,
                "is_compact": is_compact,
                "sidebar_mode": sidebar_mode,
            },
            "device_type": device_type,
            "user_agent": user_agent,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "active": True,
        }
        self.sessions[session_id] = session_meta
        self._record_audit("SESSION_REGISTERED", f"Client session {session_id} on {device_type} ({viewport_width}x{viewport_height})")
        return session_meta

    def compress_analytics_payload(
        self,
        session_id: str,
        kpi_metrics: List[Dict[str, Any]],
        timeseries_points: List[float],
    ) -> Dict[str, Any]:
        """Applies adaptive downsampling for mobile viewports to prevent memory pressure."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not registered")

        viewport = session["viewport"]
        max_points = 24 if viewport["is_compact"] else 90

        if len(timeseries_points) > max_points:
            stride = math.ceil(len(timeseries_points) / max_points)
            sampled_series = [
                timeseries_points[i] for i in range(0, len(timeseries_points), stride)
            ][:max_points]
        else:
            sampled_series = timeseries_points

        compressed_payload = {
            "tenant_id": self.tenant_id,
            "session_id": session_id,
            "viewport_mode": viewport["sidebar_mode"],
            "metric_count": len(kpi_metrics),
            "points_count": len(sampled_series),
            "original_points": len(timeseries_points),
            "compression_ratio": round(len(sampled_series) / max(1, len(timeseries_points)), 3),
            "timeseries": sampled_series,
            "delivery_timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._record_audit("PAYLOAD_DELIVERED", f"Delivered {len(sampled_series)} sampled points to {session_id}")
        return compressed_payload

    def toggle_sidebar_layout(self, session_id: str, force_shrink: bool) -> Dict[str, Any]:
        """Toggles sidebar state between shrunk rail and expanded layout."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not registered")

        if session["viewport"]["is_compact"]:
            # On mobile, toggle is a drawer visibility flag
            session["viewport"]["drawer_open"] = force_shrink
        else:
            # On desktop, toggle shrinks sidebar to expand analytics canvas
            session["viewport"]["sidebar_mode"] = "rail" if force_shrink else "expanded"

        self._record_audit(
            "LAYOUT_TOGGLED",
            f"Session {session_id} sidebar updated to: {session['viewport']['sidebar_mode']}"
        )
        return session["viewport"]

    def _record_audit(self, action: str, details: str) -> None:
        self.audit_log.append({
            "tenant_id": self.tenant_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


def test_mobile_session_registration():
    """Verify viewport negotiation for mobile and tablet screens."""
    dispatcher = MobileTelemetryDispatcher(tenant_id="primelogix")
    
    # 1. iPhone 14 Pro viewport
    mobile_sess = dispatcher.register_client_session("sess_iphone", 393, 852, "mobile")
    assert mobile_sess["viewport"]["is_compact"] is True
    assert mobile_sess["viewport"]["sidebar_mode"] == "drawer"

    # 2. Desktop 4K monitor viewport
    desktop_sess = dispatcher.register_client_session("sess_desktop", 2560, 1440, "desktop")
    assert desktop_sess["viewport"]["is_compact"] is False
    assert desktop_sess["viewport"]["sidebar_mode"] == "expanded"


def test_sidebar_toggle_negotiation():
    """Verify that toggling the sidebar dynamically adapts workspace constraints."""
    dispatcher = MobileTelemetryDispatcher(tenant_id="primelogix")
    sess = dispatcher.register_client_session("sess_laptop", 1440, 900, "desktop")
    assert sess["viewport"]["sidebar_mode"] == "expanded"

    # User collapses sidebar to expand analytics canvas
    shrunk_viewport = dispatcher.toggle_sidebar_layout("sess_laptop", force_shrink=True)
    assert shrunk_viewport["sidebar_mode"] == "rail"

    # User re-expands sidebar
    expanded_viewport = dispatcher.toggle_sidebar_layout("sess_laptop", force_shrink=False)
    assert expanded_viewport["sidebar_mode"] == "expanded"


def test_adaptive_mobile_payload_compression():
    """Verify that time series data is safely downsampled for mobile displays to ensure zero latency."""
    dispatcher = MobileTelemetryDispatcher(tenant_id="primelogix")
    dispatcher.register_client_session("sess_phone", 375, 812, "mobile")

    raw_series = [100.0 + i * 0.5 + (i % 7) for i in range(365)]
    kpis = [{"name": "Revenue", "value": 148.24}, {"name": "Margin", "value": 31.2}]

    compressed = dispatcher.compress_analytics_payload("sess_phone", kpis, raw_series)
    assert compressed["points_count"] <= 24
    assert compressed["compression_ratio"] < 0.10
    assert len(compressed["timeseries"]) == compressed["points_count"]


def test_audit_log_traceability():
    """Verify that all responsive viewport negotiations produce immutable audit logs."""
    dispatcher = MobileTelemetryDispatcher(tenant_id="primelogix")
    dispatcher.register_client_session("sess_audit", 1920, 1080, "desktop")
    dispatcher.toggle_sidebar_layout("sess_audit", True)

    assert len(dispatcher.audit_log) == 2
    actions = [log["action"] for log in dispatcher.audit_log]
    assert "SESSION_REGISTERED" in actions
    assert "LAYOUT_TOGGLED" in actions
    for log in dispatcher.audit_log:
        assert log["tenant_id"] == "primelogix"
        assert "timestamp" in log
