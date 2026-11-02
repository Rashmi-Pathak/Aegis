"""AEGIS Operations & Logistics Performance Engine
Computes On-Time In-Full (OTIF), Fleet Capacity Utilization, Turnaround Times,
and Route Dwell Variances.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd


class OperationsAnalytics:
    """Fleet logistics, freight dispatch, and SLA compliance analytics."""

    @staticmethod
    def calculate_otif(
        total_shipments: int,
        on_time_shipments: int,
        in_full_shipments: int,
        damage_free_shipments: int,
    ) -> Dict[str, Any]:
        """Calculates On-Time In-Full (OTIF) and Perfect Order Index (POI)."""
        if total_shipments <= 0:
            return {"otif_pct": 0.0, "poi_pct": 0.0, "status": "No Shipments"}

        on_time_pct = (on_time_shipments / total_shipments) * 100.0
        in_full_pct = (in_full_shipments / total_shipments) * 100.0
        damage_free_pct = (damage_free_shipments / total_shipments) * 100.0

        # Perfect Order Index = On-Time% * In-Full% * Damage-Free%
        poi = (on_time_pct / 100.0) * (in_full_pct / 100.0) * (damage_free_pct / 100.0) * 100.0
        otif = min(on_time_pct, in_full_pct)

        status = "Optimal"
        if otif < 85.0:
            status = "Breach Risk"
        elif otif < 92.0:
            status = "Degraded Reliability"

        return {
            "total_shipments": total_shipments,
            "on_time_pct": round(on_time_pct, 1),
            "in_full_pct": round(in_full_pct, 1),
            "damage_free_pct": round(damage_free_pct, 1),
            "otif_compliance_pct": round(otif, 1),
            "perfect_order_index_pct": round(poi, 1),
            "sla_status": status,
        }

    @staticmethod
    def analyze_fleet_utilization(
        active_assets: int,
        total_fleet_capacity: int,
        idle_assets: int,
        maintenance_assets: int,
    ) -> Dict[str, Any]:
        """Calculates utilization rates and maintenance downtime ratios."""
        if total_fleet_capacity <= 0:
            return {"utilization_pct": 0.0, "availability_pct": 0.0}

        util_pct = (active_assets / total_fleet_capacity) * 100.0
        avail_pct = ((total_fleet_capacity - maintenance_assets) / total_fleet_capacity) * 100.0
        idle_pct = (idle_assets / total_fleet_capacity) * 100.0

        return {
            "active_fleet_utilization_pct": round(util_pct, 1),
            "fleet_availability_pct": round(avail_pct, 1),
            "idle_capacity_pct": round(idle_pct, 1),
            "maintenance_ratio_pct": round((maintenance_assets / total_fleet_capacity) * 100.0, 1),
        }
