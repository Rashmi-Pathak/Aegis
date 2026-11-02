"""AEGIS Decision Impact & Counterfactual Uplift Estimator
Quantifies expected margin delta, cost reduction, and operational recovery for decision candidates.
"""
from typing import Dict, Any, List

class DecisionImpactEstimator:
    @staticmethod
    def estimate_initiative_impact(
        baseline_revenue: float,
        baseline_cost: float,
        cost_reduction_pct: float,
        revenue_uplift_pct: float,
        implementation_cost: float,
    ) -> Dict[str, Any]:
        """Calculates net economic value added and margin expansion."""
        cost_savings = baseline_cost * (cost_reduction_pct / 100.0)
        revenue_gains = baseline_revenue * (revenue_uplift_pct / 100.0)
        gross_annual_benefit = cost_savings + revenue_gains
        net_first_year_value = gross_annual_benefit - implementation_cost

        old_margin = ((baseline_revenue - baseline_cost) / baseline_revenue) * 100.0 if baseline_revenue > 0 else 0.0
        new_rev = baseline_revenue + revenue_gains
        new_cost = baseline_cost - cost_savings
        new_margin = ((new_rev - new_cost) / new_rev) * 100.0 if new_rev > 0 else 0.0

        return {
            "first_year_net_value": round(net_first_year_value, 2),
            "annual_recurring_benefit": round(gross_annual_benefit, 2),
            "margin_expansion_bps": round((new_margin - old_margin) * 100.0, 1),
            "payback_period_months": round((implementation_cost / (gross_annual_benefit / 12.0)), 1) if gross_annual_benefit > 0 else 999.0,
            "is_value_accretive": bool(net_first_year_value > 0),
        }
