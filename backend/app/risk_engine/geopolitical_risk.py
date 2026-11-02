"""AEGIS Geopolitical, Tariff & Maritime Choke Point Risk Engine
Models tariff escalation shocks, sanctions compliance exposure, and strait passage blockades (Suez, Malacca, Hormuz).
"""
from typing import Dict, Any, List

class GeopoliticalRiskEngine:
    CHOKE_POINTS = {
        "suez_canal": {"name": "Suez Canal / Red Sea", "base_delay_days": 14.0, "reroute_cost_per_teu": 850.0},
        "panama_canal": {"name": "Panama Canal (Drought Restriction)", "base_delay_days": 8.0, "reroute_cost_per_teu": 420.0},
        "malacca_strait": {"name": "Strait of Malacca", "base_delay_days": 18.0, "reroute_cost_per_teu": 1100.0},
    }

    @classmethod
    def evaluate_freight_rerouting_shock(
        cls,
        choke_point_key: str,
        annual_teu_volume: float,
        active_blockade_status: bool = True,
        tariff_escalation_pct: float = 15.0,
        cargo_value_usd: float = 50000000.0,
    ) -> Dict[str, Any]:
        """Calculates supply chain detour expense and tariff margin compression."""
        point = cls.CHOKE_POINTS.get(choke_point_key, cls.CHOKE_POINTS["suez_canal"])

        reroute_expense = annual_teu_volume * point["reroute_cost_per_teu"] if active_blockade_status else 0.0
        tariff_expense = cargo_value_usd * (tariff_escalation_pct / 100.0)
        total_geopolitical_drag = reroute_expense + tariff_expense

        return {
            "choke_point": point["name"],
            "transit_delay_days": point["base_delay_days"] if active_blockade_status else 0.0,
            "annual_rerouting_cost_usd": round(reroute_expense, 2),
            "tariff_duty_impact_usd": round(tariff_expense, 2),
            "total_geopolitical_financial_drag": round(total_geopolitical_drag, 2),
            "mitigation_recommendation": "Activate Cape of Good Hope long-term volume hedging & nearshore suppliers",
        }
