"""AEGIS Earned Value Management (EVM) Project Health Engine
Computes PV, EV, AC, Cost Variance (CV), Schedule Variance (SV), CPI, SPI, and Estimate at Completion (EAC).
"""
from typing import Dict, Any, List

class EVMAnalysisEngine:
    @staticmethod
    def compute_evm_metrics(
        planned_value_pv: float,
        earned_value_ev: float,
        actual_cost_ac: float,
        budget_at_completion_bac: float,
    ) -> Dict[str, Any]:
        """Calculates standard ANSI/EIA-748 Earned Value Management indices."""
        cost_variance = earned_value_ev - actual_cost_ac
        schedule_variance = earned_value_ev - planned_value_pv

        cpi = round(earned_value_ev / actual_cost_ac, 3) if actual_cost_ac > 0 else 1.0
        spi = round(earned_value_ev / planned_value_pv, 3) if planned_value_pv > 0 else 1.0

        # Estimate At Completion (EAC) assuming current cost efficiency continues
        eac = round(budget_at_completion_bac / cpi, 2) if cpi > 0 else budget_at_completion_bac
        variance_at_completion = round(budget_at_completion_bac - eac, 2)

        # To Complete Performance Index (TCPI) to stay within budget
        remaining_work = budget_at_completion_bac - earned_value_ev
        remaining_funds = budget_at_completion_bac - actual_cost_ac
        tcpi = round(remaining_work / remaining_funds, 3) if remaining_funds > 0 else 999.0

        health = "On Track"
        if cpi < 0.85 or spi < 0.85:
            health = "Critical Project Distress (Severe Overrun/Delay)"
        elif cpi < 0.95 or spi < 0.95:
            health = "Warning: Sub-Optimal Efficiency"

        return {
            "planned_value_pv": planned_value_pv,
            "earned_value_ev": earned_value_ev,
            "actual_cost_ac": actual_cost_ac,
            "budget_at_completion_bac": budget_at_completion_bac,
            "cost_variance_cv": round(cost_variance, 2),
            "schedule_variance_sv": round(schedule_variance, 2),
            "cost_performance_index_cpi": cpi,
            "schedule_performance_index_spi": spi,
            "estimate_at_completion_eac": eac,
            "variance_at_completion_vac": variance_at_completion,
            "to_complete_performance_index_tcpi": tcpi,
            "project_health_status": health,
        }
