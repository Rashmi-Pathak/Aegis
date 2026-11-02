"""AEGIS Macroeconomic Scenario Stress Testing Engine
Applies multi-factor macroeconomic stress scenarios to enterprise balance sheets and P&L.
"""

from typing import List, Dict, Any


class MacroStressTester:
    """Simulates systemic macroeconomic headwinds: Stagflation, Energy Shock, Rate Hike."""

    SCENARIOS = {
        "stagflation_shock": {
            "name": "Global Stagflation & Demand Contraction",
            "revenue_shock_pct": -12.5,
            "cost_inflation_pct": 14.0,
            "interest_rate_delta_bps": 250,
            "fuel_spike_pct": 35.0,
        },
        "energy_crisis": {
            "name": "Geopolitical Energy & Bunker Fuel Surge",
            "revenue_shock_pct": -2.0,
            "cost_inflation_pct": 8.0,
            "interest_rate_delta_bps": 50,
            "fuel_spike_pct": 55.0,
        },
        "supply_chain_freeze": {
            "name": "Global Maritime Choke & Port Gridlock",
            "revenue_shock_pct": -18.0,
            "cost_inflation_pct": 22.0,
            "interest_rate_delta_bps": 100,
            "fuel_spike_pct": 20.0,
        },
    }

    @classmethod
    def apply_scenario(
        cls,
        scenario_key: str,
        baseline_revenue: float,
        baseline_ebitda: float,
        annual_fuel_spend: float,
        debt_principal: float,
    ) -> Dict[str, Any]:
        """Projects financial impact under selected stress scenario."""
        scen = cls.SCENARIOS.get(scenario_key, cls.SCENARIOS["energy_crisis"])

        stressed_rev = baseline_revenue * (1.0 + (scen["revenue_shock_pct"] / 100.0))

        # Fuel cost delta
        fuel_delta = annual_fuel_spend * (scen["fuel_spike_pct"] / 100.0)

        # General cost inflation on non-fuel OpEx
        other_opex = max(0.0, (baseline_revenue - baseline_ebitda) - annual_fuel_spend)
        opex_inflation = other_opex * (scen["cost_inflation_pct"] / 100.0)

        # Interest rate hike expense
        interest_delta = debt_principal * (scen["interest_rate_delta_bps"] / 10000.0)

        total_cost_increase = fuel_delta + opex_inflation + interest_delta
        stressed_ebitda = (baseline_ebitda + (stressed_rev - baseline_revenue)) - total_cost_increase
        ebitda_delta = stressed_ebitda - baseline_ebitda

        margin_baseline = (baseline_ebitda / baseline_revenue) * 100.0 if baseline_revenue > 0 else 0.0
        margin_stressed = (stressed_ebitda / stressed_rev) * 100.0 if stressed_rev > 0 else 0.0

        return {
            "scenario_name": scen["name"],
            "baseline_revenue": round(baseline_revenue, 2),
            "stressed_revenue": round(stressed_rev, 2),
            "baseline_ebitda": round(baseline_ebitda, 2),
            "stressed_ebitda": round(stressed_ebitda, 2),
            "ebitda_impact_delta": round(ebitda_delta, 2),
            "margin_compression_bps": round((margin_baseline - margin_stressed) * 100.0, 1),
            "is_ebitda_positive": bool(stressed_ebitda > 0),
            "recommended_cushion_reserve": round(abs(min(0.0, stressed_ebitda)) + (baseline_revenue * 0.05), 2),
        }
