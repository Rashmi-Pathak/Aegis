"""
Tests for ViewportOptimizer and responsive break-point resolution.
Verifies grid sizing, usable canvas calculation, touch optimization flags, and matrix downsampling.
"""

import pytest
from app.analytics.mobile_viewport_optimizer import ViewportOptimizer


def test_resolve_spec_breakpoints():
    """Verify resolution of standard device widths into appropriate specs."""
    # Mobile iPhone 14
    spec_iphone = ViewportOptimizer.resolve_spec(393)
    assert spec_iphone.breakpoint_name == "xs"
    assert spec_iphone.enable_mobile_drawer is True
    assert spec_iphone.recommended_columns == 1

    # iPad / Tablet
    spec_tablet = ViewportOptimizer.resolve_spec(820)
    assert spec_tablet.breakpoint_name == "md"
    assert spec_tablet.recommended_columns == 2

    # Desktop 1080p
    spec_desktop = ViewportOptimizer.resolve_spec(1920)
    assert spec_desktop.breakpoint_name == "2xl"
    assert spec_desktop.enable_compact_rail is True
    assert spec_desktop.recommended_columns == 4


def test_calculate_analytics_grid_desktop_expansion():
    """Verify that shrinking the sidebar increases the usable canvas width."""
    width = 1440
    # 1. Expanded sidebar
    grid_expanded = ViewportOptimizer.calculate_analytics_grid(width, is_sidebar_collapsed=False)
    assert grid_expanded["sidebar_width_px"] == 256
    assert grid_expanded["sidebar_mode"] == "expanded"

    # 2. Collapsed / Shrunk sidebar
    grid_shrunk = ViewportOptimizer.calculate_analytics_grid(width, is_sidebar_collapsed=True)
    assert grid_shrunk["sidebar_width_px"] == 72
    assert grid_shrunk["sidebar_mode"] == "rail"

    # The canvas must gain exactly 256 - 72 = 184 pixels of width
    assert grid_shrunk["usable_canvas_px"] - grid_expanded["usable_canvas_px"] == 184


def test_downsample_matrix():
    """Verify that large heatmaps downsample smoothly without exceeding mobile limits."""
    # Create a 50x50 correlation matrix
    large_matrix = [[float(i * j) for j in range(50)] for i in range(50)]
    downsampled = ViewportOptimizer.downsample_matrix(large_matrix, max_dim=8)

    assert len(downsampled) == 8
    assert len(downsampled[0]) == 8
    assert downsampled[0][0] == 0.0
