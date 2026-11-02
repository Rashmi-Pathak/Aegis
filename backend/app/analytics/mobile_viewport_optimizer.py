"""
AEGIS — Mobile Viewport & Latency Optimization Service.
Calculates dynamic CSS layout constraints, bandwidth-optimized chart downsampling,
and responsive break-points for enterprise client devices.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ViewportSpec:
    breakpoint_name: str
    min_width: int
    max_width: int
    recommended_columns: int
    enable_compact_rail: bool
    enable_mobile_drawer: bool
    max_timeseries_points: int


VIEWPORT_BREAKPOINTS: Dict[str, ViewportSpec] = {
    "xs": ViewportSpec("xs", 0, 639, 1, False, True, 18),
    "sm": ViewportSpec("sm", 640, 767, 2, False, True, 24),
    "md": ViewportSpec("md", 768, 1023, 2, False, True, 36),
    "lg": ViewportSpec("lg", 1024, 1279, 3, True, False, 60),
    "xl": ViewportSpec("xl", 1280, 1535, 4, True, False, 90),
    "2xl": ViewportSpec("2xl", 1536, 99999, 4, True, False, 180),
}


class ViewportOptimizer:
    """Provides client-tailored layout recommendations and zero-latency downsampling configurations."""

    @staticmethod
    def resolve_spec(width: int) -> ViewportSpec:
        """Resolves target ViewportSpec based on raw pixel width."""
        for spec in VIEWPORT_BREAKPOINTS.values():
            if spec.min_width <= width <= spec.max_width:
                return spec
        return VIEWPORT_BREAKPOINTS["xl"]

    @staticmethod
    def calculate_analytics_grid(width: int, is_sidebar_collapsed: bool = False) -> Dict[str, Any]:
        """Calculates optimal grid columns and canvas width allocation."""
        spec = ViewportOptimizer.resolve_spec(width)
        sidebar_width = 0 if spec.enable_mobile_drawer else (72 if is_sidebar_collapsed else 256)
        usable_canvas_width = max(320, width - sidebar_width - 32)

        return {
            "breakpoint": spec.breakpoint_name,
            "sidebar_mode": "drawer" if spec.enable_mobile_drawer else ("rail" if is_sidebar_collapsed else "expanded"),
            "sidebar_width_px": sidebar_width,
            "usable_canvas_px": usable_canvas_width,
            "recommended_columns": spec.recommended_columns,
            "max_chart_points": spec.max_timeseries_points,
            "enable_touch_optimizations": spec.enable_mobile_drawer,
        }

    @staticmethod
    def generate_responsive_css_variables(width: int, is_sidebar_collapsed: bool = False) -> Dict[str, str]:
        """Generates inline CSS custom properties for hardware-accelerated fluid sizing."""
        grid_spec = ViewportOptimizer.calculate_analytics_grid(width, is_sidebar_collapsed)
        return {
            "--aegis-sidebar-w": f"{grid_spec['sidebar_width_px']}px",
            "--aegis-canvas-w": f"{grid_spec['usable_canvas_px']}px",
            "--aegis-grid-cols": str(grid_spec["recommended_columns"]),
            "--aegis-transition-speed": "300ms",
            "--aegis-transition-easing": "cubic-bezier(0.16, 1, 0.3, 1)",
        }

    @staticmethod
    def estimate_render_budget_ms(viewport_width: int, data_points: int) -> float:
        """Estimates frame execution budget in milliseconds to guarantee 60fps performance."""
        spec = ViewportOptimizer.resolve_spec(viewport_width)
        base_budget = 16.67  # 60fps frame budget
        penalty = max(0.0, (data_points - spec.max_timeseries_points) * 0.05)
        return max(4.0, base_budget - penalty)

    @staticmethod
    def downsample_matrix(matrix: List[List[float]], max_dim: int = 12) -> List[List[float]]:
        """Downsamples a 2D risk/heatmap correlation matrix for fluid mobile rendering."""
        if not matrix or len(matrix) <= max_dim:
            return matrix

        step = len(matrix) / max_dim
        sampled: List[List[float]] = []
        for i in range(max_dim):
            r_idx = min(len(matrix) - 1, int(i * step))
            row = matrix[r_idx]
            if len(row) <= max_dim:
                sampled.append(row)
            else:
                c_step = len(row) / max_dim
                sampled_row = [row[min(len(row) - 1, int(j * c_step))] for j in range(max_dim)]
                sampled.append(sampled_row)
        return sampled
