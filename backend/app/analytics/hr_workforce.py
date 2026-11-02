"""AEGIS Human Capital & Workforce Attrition Analytics
Models talent turnover velocity, revenue per employee, and mission-critical role vacancy risk.
"""

from typing import List, Dict, Any
import numpy as np


class WorkforceAnalytics:
    """Human capital productivity, turnover hazard, and critical skill gap modeling."""

    @staticmethod
    def calculate_workforce_kpis(
        total_headcount: int,
        annualized_revenue: float,
        annualized_payroll: float,
        departures_last_12m: int,
        critical_role_openings: int,
    ) -> Dict[str, Any]:
        """Calculates Revenue Per Employee, Labor Cost Ratio, and Annual Turnover Rate."""
        if total_headcount <= 0:
            return {"status": "No Active Workforce"}

        rev_per_emp = annualized_revenue / total_headcount
        payroll_ratio = (annualized_payroll / annualized_revenue) * 100.0 if annualized_revenue > 0 else 0.0
        turnover_rate = (departures_last_12m / total_headcount) * 100.0

        risk_level = "Normal"
        if turnover_rate > 22.0 or (critical_role_openings / total_headcount) > 0.08:
            risk_level = "Severe Workforce Disruption Risk"
        elif turnover_rate > 15.0:
            risk_level = "Elevated Talent Churn"

        return {
            "total_headcount": total_headcount,
            "revenue_per_employee_usd": round(rev_per_emp, 2),
            "payroll_to_revenue_pct": round(payroll_ratio, 2),
            "annualized_turnover_rate_pct": round(turnover_rate, 2),
            "critical_role_vacancy_count": critical_role_openings,
            "workforce_stability_status": risk_level,
        }
