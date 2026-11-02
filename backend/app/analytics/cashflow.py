"""AEGIS Cash Flow, Runway & Liquidity Burn Analytics
Simulates enterprise cash burn, liquidity runway, and operating cash conversion.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class CashFlowAnalytics:
    """Working capital liquidity, direct cash flow trajectory, and treasury risk analytics."""

    @staticmethod
    def calculate_burn_and_runway(
        current_cash_reserve: float,
        monthly_cash_burns: List[float],
        growth_capital_commitments: float = 0.0,
    ) -> Dict[str, Any]:
        """Calculates Average Monthly Burn, Net Runway (months), and Critical Cash Breaches."""
        if not monthly_cash_burns:
            return {"runway_months": 999.0, "status": "Stable"}

        burns = np.array(monthly_cash_burns, dtype=float)
        avg_burn = float(np.mean(burns))
        recent_burn = float(burns[-1]) if len(burns) > 0 else avg_burn

        effective_cash = max(0.0, current_cash_reserve - growth_capital_commitments)

        runway_avg = round(effective_cash / avg_burn, 1) if avg_burn > 0 else 999.0
        runway_recent = round(effective_cash / recent_burn, 1) if recent_burn > 0 else 999.0

        if runway_recent < 6.0:
            status = "Immediate Liquidity Crisis (<6 Months)"
        elif runway_recent < 12.0:
            status = "Caution: Runway Under 12 Months"
        elif runway_recent < 24.0:
            status = "Adequate Operational Cushion"
        else:
            status = "Highly Capitalized Buffer"

        # Trajectory forecast
        projected_balances = []
        bal = effective_cash
        for m in range(1, 13):
            bal = max(0.0, bal - recent_burn)
            projected_balances.append({"month": m, "projected_cash": round(bal, 2)})

        return {
            "current_cash_reserve": round(current_cash_reserve, 2),
            "effective_uncommitted_cash": round(effective_cash, 2),
            "average_monthly_burn": round(avg_burn, 2),
            "most_recent_monthly_burn": round(recent_burn, 2),
            "runway_months_based_on_avg": runway_avg,
            "runway_months_based_on_recent": runway_recent,
            "liquidity_status": status,
            "projected_12_month_cash_reserve": projected_balances,
        }
