"""AEGIS Marketing Efficiency & Pipeline Attribution Engine
Calculates CAC efficiency curves, multi-touch attribution, and pipeline velocity.
"""

from typing import Dict, Any, List
import numpy as np


class MarketingAnalytics:
    """Enterprise demand generation, CAC attribution, and pipeline velocity modeling."""

    @staticmethod
    def calculate_pipeline_velocity(
        qualified_opportunities: int,
        average_deal_size: float,
        win_rate_pct: float,
        sales_cycle_days: float,
    ) -> Dict[str, Any]:
        """Pipeline Velocity = (Opps * DealSize * WinRate) / SalesCycleDays
        Measures expected revenue generated per calendar day.
        """
        if sales_cycle_days <= 0:
            return {"daily_velocity": 0.0, "monthly_expected_pipeline": 0.0}

        win_rate_decimal = win_rate_pct / 100.0
        daily_velocity = (qualified_opportunities * average_deal_size * win_rate_decimal) / sales_cycle_days
        monthly_velocity = daily_velocity * 30.0

        return {
            "daily_pipeline_velocity": round(daily_velocity, 2),
            "monthly_expected_pipeline": round(monthly_velocity, 2),
            "win_rate_pct": win_rate_pct,
            "average_deal_size": average_deal_size,
            "sales_cycle_days": sales_cycle_days,
        }

    @staticmethod
    def calculate_blended_roas(
        attributed_revenue: float,
        marketing_spend: float,
    ) -> float:
        """Return on Ad Spend (ROAS) = Attributed Revenue / Marketing Spend"""
        if marketing_spend <= 0:
            return 0.0
        return round(attributed_revenue / marketing_spend, 2)
