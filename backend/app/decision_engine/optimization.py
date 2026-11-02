"""AEGIS Decision Intelligence & Constrained Portfolio Optimization
Formulates capital allocation, hedging allocations, and intervention decisions under risk limits.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class DecisionOptimizer:
    """Solves bounded resource allocation problems to maximize risk-adjusted ROI."""

    @staticmethod
    def allocate_hedging_budget(
        total_budget: float,
        hedging_instruments: List[Dict[str, Any]],  # name, cost_per_unit, risk_mitigated_per_unit, max_units
    ) -> Dict[str, Any]:
        """Greedy knapsack / linear approximation for risk mitigation budgeting."""
        if total_budget <= 0 or not hedging_instruments:
            return {"allocated_budget": 0.0, "total_risk_reduced": 0.0, "plan": []}

        # Calculate efficiency ratio: risk_mitigated / cost
        scored = []
        for inst in hedging_instruments:
            cost = inst.get("cost_per_unit", 1.0)
            benefit = inst.get("risk_mitigated_per_unit", 1.0)
            ratio = benefit / cost if cost > 0 else 0.0
            scored.append({**inst, "efficiency_ratio": ratio})

        # Sort by efficiency descending
        scored.sort(key=lambda x: x["efficiency_ratio"], reverse=True)

        remaining_budget = total_budget
        total_risk_reduced = 0.0
        allocation_plan = []

        for inst in scored:
            cost = inst["cost_per_unit"]
            max_u = inst.get("max_units", 100)
            if cost <= 0:
                continue

            affordable_units = min(max_u, int(remaining_budget // cost))
            if affordable_units > 0:
                spend = affordable_units * cost
                mitigation = affordable_units * inst["risk_mitigated_per_unit"]
                remaining_budget -= spend
                total_risk_reduced += mitigation
                allocation_plan.append({
                    "instrument": inst["name"],
                    "units": affordable_units,
                    "expenditure": round(spend, 2),
                    "risk_points_mitigated": round(mitigation, 1),
                })

        return {
            "total_budget": round(total_budget, 2),
            "allocated_expenditure": round(total_budget - remaining_budget, 2),
            "unallocated_cash": round(remaining_budget, 2),
            "total_risk_points_reduced": round(total_risk_reduced, 1),
            "allocation_plan": allocation_plan,
        }
