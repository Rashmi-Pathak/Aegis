"""AEGIS Intermittent & Seasonal Demand Forecaster
Implements Croston's method for intermittent spare parts/shipments alongside seasonal exponential smoothing.
"""
from typing import List, Dict, Any
import numpy as np

class DemandForecaster:
    @staticmethod
    def croston_intermittent_forecast(
        demand_history: List[float],
        horizon: int = 6,
        alpha: float = 0.2,
    ) -> Dict[str, Any]:
        """Croston's method separates demand non-zero size from inter-arrival intervals."""
        non_zero_sizes = []
        intervals = []
        last_idx = -1

        for i, val in enumerate(demand_history):
            if val > 0:
                non_zero_sizes.append(val)
                if last_idx >= 0:
                    intervals.append(i - last_idx)
                last_idx = i

        if not non_zero_sizes:
            return {"forecast_rate": [0.0] * horizon, "intermittent": True}

        # Smooth size
        z = non_zero_sizes[0]
        for val in non_zero_sizes[1:]:
            z = alpha * val + (1.0 - alpha) * z

        # Smooth intervals
        p = intervals[0] if intervals else 1.0
        for val in intervals[1:]:
            p = alpha * val + (1.0 - alpha) * p

        rate = z / p if p > 0 else z

        return {
            "estimated_demand_per_period": round(float(rate), 2),
            "forecast": [round(float(rate), 2)] * horizon,
            "average_demand_magnitude": round(float(z), 2),
            "average_inter_arrival_intervals": round(float(p), 2),
            "is_intermittent": bool(len(non_zero_sizes) < len(demand_history) * 0.7),
        }
