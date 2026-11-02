"""AEGIS Inventory Analytics & Supply Chain Buffering
Calculates Economic Order Quantity (EOQ), Safety Stock targets, Days of Supply,
and Stockout Probabilities.
"""

from typing import Dict, Any, List
import numpy as np
import scipy.stats as stats


class InventoryAnalytics:
    """Supply chain inventory buffer modeling and lead-time variability analysis."""

    @staticmethod
    def calculate_eoq(
        annual_demand: float,
        ordering_cost_fixed: float,
        annual_holding_cost_per_unit: float,
    ) -> Dict[str, float]:
        """Economic Order Quantity (Wilson Formula):
        EOQ = sqrt((2 * Demand * OrderCost) / HoldingCost)
        """
        if annual_holding_cost_per_unit <= 0 or annual_demand <= 0:
            return {"eoq": 0.0, "optimal_orders_per_year": 0.0, "total_cost": 0.0}

        eoq = np.sqrt((2.0 * annual_demand * ordering_cost_fixed) / annual_holding_cost_per_unit)
        orders_per_year = annual_demand / eoq
        annual_order_cost = orders_per_year * ordering_cost_fixed
        annual_holding_cost = (eoq / 2.0) * annual_holding_cost_per_unit
        total_cost = annual_order_cost + annual_holding_cost

        return {
            "economic_order_quantity": round(float(eoq), 1),
            "optimal_orders_per_year": round(float(orders_per_year), 1),
            "annual_order_cost": round(float(annual_order_cost), 2),
            "annual_holding_cost": round(float(annual_holding_cost), 2),
            "total_inventory_cost": round(float(total_cost), 2),
        }

    @staticmethod
    def calculate_safety_stock(
        daily_demand_mean: float,
        daily_demand_std: float,
        lead_time_days_mean: float,
        lead_time_days_std: float,
        target_service_level_pct: float = 95.0,
    ) -> Dict[str, float]:
        """Safety stock with stochastic demand AND stochastic supplier lead times:
        SS = Z * sqrt( (LeadTime * StdDemand^2) + (Demand^2 * StdLeadTime^2) )
        """
        z_score = stats.norm.ppf(target_service_level_pct / 100.0)

        variance_demand_during_lt = (
            (lead_time_days_mean * (daily_demand_std ** 2))
            + ((daily_demand_mean ** 2) * (lead_time_days_std ** 2))
        )
        safety_stock = z_score * np.sqrt(variance_demand_during_lt)
        reorder_point = (daily_demand_mean * lead_time_days_mean) + safety_stock

        return {
            "service_level_z": round(float(z_score), 3),
            "recommended_safety_stock_units": round(float(safety_stock), 1),
            "reorder_point_units": round(float(reorder_point), 1),
            "lead_time_buffer_days": round(float(safety_stock / daily_demand_mean), 1) if daily_demand_mean > 0 else 0.0,
        }

    @staticmethod
    def days_of_inventory_on_hand(current_stock_units: float, average_daily_usage: float) -> float:
        """DOH = Stock / Daily Usage"""
        if average_daily_usage <= 0:
            return 999.0
        return round(current_stock_units / average_daily_usage, 1)
