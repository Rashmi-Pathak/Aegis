"""AEGIS Activity-Based Costing (ABC) & Cost Center Variance Engine
Allocates corporate overhead to product lines, sales channels, and geographic business units.
"""
from typing import Dict, Any, List
import numpy as np

class ActivityBasedCostingEngine:
    @staticmethod
    def allocate_overhead(
        total_overhead_pool_usd: float,
        cost_drivers: List[Dict[str, Any]],  # activity, driver_name, units_consumed, cost_per_driver_unit
    ) -> Dict[str, Any]:
        """Allocates corporate overhead pools based on consumption rates."""
        allocated_activities = []
        total_allocated = 0.0

        for d in cost_drivers:
            activity = d.get("activity", "General Overhead")
            units = d.get("units_consumed", 0.0)
            rate = d.get("cost_per_driver_unit", 1.0)
            cost = units * rate
            total_allocated += cost
            allocated_activities.append({
                "activity": activity,
                "driver": d.get("driver_name", "Units"),
                "allocated_amount_usd": round(cost, 2),
            })

        unallocated = max(0.0, total_overhead_pool_usd - total_allocated)

        return {
            "total_overhead_pool_usd": round(total_overhead_pool_usd, 2),
            "total_allocated_usd": round(total_allocated, 2),
            "unallocated_variance_usd": round(unallocated, 2),
            "allocated_breakdown": allocated_activities,
            "absorption_rate_pct": round((total_allocated / total_overhead_pool_usd) * 100.0, 1) if total_overhead_pool_usd > 0 else 100.0,
        }
