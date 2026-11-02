"""AEGIS Global Tariff Escalation & Trade War Simulation Engine
Models multi-country reciprocal tariff imposition and raw material supply reallocation.
"""
from typing import Dict, Any, List
import numpy as np

class TradeWarSimulationEngine:
    @staticmethod
    def simulate_bilateral_tariff_shock(
        annual_import_volume_usd: float,
        annual_export_volume_usd: float,
        baseline_gross_margin_pct: float,
        import_tariff_rate_pct: float = 25.0,
        retaliatory_export_tariff_rate_pct: float = 15.0,
        supplier_absorption_rate_pct: float = 20.0,
        customer_pass_through_rate_pct: float = 50.0,
    ) -> Dict[str, Any]:
        """Projects margin impact of international trade protectionism."""
        gross_import_duty = annual_import_volume_usd * (import_tariff_rate_pct / 100.0)
        absorbed_by_supplier = gross_import_duty * (supplier_absorption_rate_pct / 100.0)
        net_import_cost_surge = gross_import_duty - absorbed_by_supplier

        passed_to_customer = net_import_cost_surge * (customer_pass_through_rate_pct / 100.0)
        unabsorbed_cost_drag = net_import_cost_surge - passed_to_customer

        # Export demand contraction from retaliatory duties
        export_demand_loss = annual_export_volume_usd * (retaliatory_export_tariff_rate_pct / 100.0) * 0.85

        total_profit_erosion = unabsorbed_cost_drag + (export_demand_loss * (baseline_gross_margin_pct / 100.0))

        return {
            "gross_tariff_duty_usd": round(gross_import_duty, 2),
            "absorbed_by_supply_base_usd": round(absorbed_by_supplier, 2),
            "passed_to_end_customers_usd": round(passed_to_customer, 2),
            "net_unabsorbed_margin_drag_usd": round(unabsorbed_cost_drag, 2),
            "export_revenue_destruction_usd": round(export_demand_loss, 2),
            "total_annual_ebitda_erosion_usd": round(total_profit_erosion, 2),
            "resilience_recommendation": "Accelerate nearshoring to USMCA / ASEAN trade treaty zones",
        }
