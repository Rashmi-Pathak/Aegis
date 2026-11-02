"""AEGIS Multi-Horizon Enterprise Revenue Forecaster
Generates baseline, bull, and bear revenue projections with confidence intervals.
"""
from typing import List, Dict, Any
import numpy as np
from app.forecasting.time_series import ClassicalForecaster

class RevenueForecaster:
    @staticmethod
    def forecast_revenue_scenarios(
        historical_revenue: List[float],
        horizon_quarters: int = 4,
    ) -> Dict[str, Any]:
        """Produces 3-scenario revenue outlook (Base, High, Stressed)."""
        res = ClassicalForecaster.double_exponential_smoothing(historical_revenue, horizon=horizon_quarters)
        base = res["forecast"]
        lower = res["lower_bound"]
        upper = res["upper_bound"]

        return {
            "baseline_forecast": base,
            "bear_stressed_case": lower,
            "bull_growth_case": upper,
            "forecast_horizon_quarters": horizon_quarters,
            "trend_direction": "UPWARD" if base[-1] >= base[0] else "DOWNWARD",
        }
