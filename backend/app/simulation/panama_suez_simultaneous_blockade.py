"""AEGIS Simultaneous Dual-Canal Maritime Choke Point Simulation
Models systemic container shipping gridlock when both Panama and Suez Canals experience capacity reductions.
"""
from typing import Dict, Any, List

class DualCanalMaritimeBlockadeEngine:
    @staticmethod
    def simulate_dual_choke_point_shock(
        annual_container_teus: float,
        panama_draft_restriction_pct: float = 35.0,
        suez_diversion_cape_of_good_hope: bool = True,
        fuel_bunker_price_per_ton_usd: float = 650.0,
    ) -> Dict[str, Any]:
        """Calculates transit days added, bunker fuel consumption surge, and inventory carrying cost inflation."""
        # Suez diversion adds 12-14 sailing days around Africa
        suez_extra_days = 13.5 if suez_diversion_cape_of_good_hope else 0.0
        # Panama draft restrictions force rail landbridges or smaller vessels (+6 days)
        panama_extra_days = 6.0 * (panama_draft_restriction_pct / 30.0)

        total_extra_transit_days = suez_extra_days + panama_extra_days

        # Extra fuel: container vessels burn ~40 tons bunker fuel per extra sea day
        extra_fuel_tons = (annual_container_teus / 5000.0) * total_extra_transit_days * 35.0
        extra_bunker_cost = extra_fuel_tons * fuel_bunker_price_per_ton_usd

        # Working capital carrying cost of inventory stuck on water (assuming $50k value per TEU at 8% cost of capital)
        inventory_capital_drag = annual_container_teus * 50000.0 * (total_extra_transit_days / 365.0) * 0.08

        total_supply_chain_surcharge = extra_bunker_cost + inventory_capital_drag

        return {
            "total_extra_transit_days_average": round(total_extra_transit_days, 1),
            "additional_bunker_fuel_cost_usd": round(extra_bunker_cost, 2),
            "in_transit_inventory_capital_drag_usd": round(inventory_capital_drag, 2),
            "total_maritime_supply_chain_surcharge_usd": round(total_supply_chain_surcharge, 2),
            "carrier_otif_sla_expected_drop_pct": round(min(45.0, total_extra_transit_days * 1.8), 1),
        }
