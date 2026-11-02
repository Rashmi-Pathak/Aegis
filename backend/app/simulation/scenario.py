"""AEGIS Scenario Definition & Parameter Registry
Standard library of enterprise What-If scenarios available to executives.
"""
from typing import Dict, Any, List

class EnterpriseScenarioLibrary:
    SCENARIOS = [
        {
            "id": "fuel_shock",
            "name": "Global Diesel & Energy Benchmark Surge",
            "category": "supply_chain",
            "description": "Simulates 25% diesel spike across regional linehaul routes.",
            "default_params": {"fuel_price_hike_pct": 25.0},
        },
        {
            "id": "port_dwell_congestion",
            "name": "Major Container Hub Dwell Delays",
            "category": "operations",
            "description": "Simulates 4.5 day average dwell increase at Rotterdam & Long Beach.",
            "default_params": {"dwell_days_delta": 4.5},
        },
    ]

    @classmethod
    def list_scenarios(cls) -> List[Dict[str, Any]]:
        return cls.SCENARIOS
