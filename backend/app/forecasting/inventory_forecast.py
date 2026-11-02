"""AEGIS Inventory Depletion & Stockout Risk Forecaster
Models safety stock consumption trajectory and calculates stockout probability dates.
"""
from typing import Dict, Any, List
import numpy as np

class InventoryForecaster:
    @staticmethod
    def forecast_stock_depletion(
        current_stock: float,
        forecasted_daily_demand: List[float],
        replenishment_orders: List[Dict[str, Any]],  # day, units
    ) -> Dict[str, Any]:
        """Calculates day-by-day stock balance and flags stockout risk days."""
        trajectory = []
        stock = current_stock
        stockout_day = None

        replenish_by_day = {r.get("day", 0): r.get("units", 0) for r in replenishment_orders}

        for day, demand in enumerate(forecasted_daily_demand, start=1):
            inflow = replenish_by_day.get(day, 0.0)
            stock = stock + inflow - demand
            trajectory.append({"day": day, "stock_level": round(stock, 1), "replenishment": inflow})
            if stock <= 0 and stockout_day is None:
                stockout_day = day

        return {
            "starting_stock": current_stock,
            "projected_depletion": trajectory,
            "stockout_projected": bool(stockout_day is not None),
            "stockout_day": stockout_day,
            "minimum_stock_level": min(t["stock_level"] for t in trajectory) if trajectory else current_stock,
        }
