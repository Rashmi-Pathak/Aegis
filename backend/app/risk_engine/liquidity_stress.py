"""AEGIS Enterprise Liquidity Stress & Basel III LCR Simulation
Tests corporate liquidity buffers under severe 30-day cash outflow scenarios.
"""

from typing import Dict, Any, List


class LiquidityStressEngine:
    """Stress tests high-quality liquid assets (HQLA) against contractual and contingency outflows."""

    @staticmethod
    def simulate_30_day_liquidity_stress(
        cash_and_equivalents: float,
        committed_undrawn_credit_lines: float,
        contractual_debt_maturities_30d: float,
        operational_payables_30d: float,
        contingent_fuel_price_spike_outflow: float,
        customer_delay_receivable_haircut_pct: float = 20.0,
        expected_receivables_inflow_30d: float = 10000000.0,
    ) -> Dict[str, Any]:
        """Calculates stressed Liquidity Coverage Ratio (LCR):
        LCR = Total Liquid Assets / Stressed Net Cash Outflows (Threshold >= 100%)
        """
        total_available_liquidity = cash_and_equivalents + committed_undrawn_credit_lines

        stressed_inflow = expected_receivables_inflow_30d * (1.0 - (customer_delay_receivable_haircut_pct / 100.0))
        total_outflows = (
            contractual_debt_maturities_30d
            + operational_payables_30d
            + contingent_fuel_price_spike_outflow
        )

        net_stressed_outflow = max(1.0, total_outflows - stressed_inflow)

        lcr_ratio = round((total_available_liquidity / net_stressed_outflow) * 100.0, 1)

        if lcr_ratio >= 140.0:
            status = "Strong Liquidity Surplus"
        elif lcr_ratio >= 100.0:
            status = "Compliant Buffer"
        elif lcr_ratio >= 80.0:
            status = "Moderate Liquidity Strain"
        else:
            status = "Critical Liquidity Breach Risk"

        return {
            "total_available_liquidity": round(total_available_liquidity, 2),
            "stressed_net_cash_outflow": round(net_stressed_outflow, 2),
            "liquidity_coverage_ratio_pct": lcr_ratio,
            "liquidity_cushion_status": status,
            "net_surplus_deficit": round(total_available_liquidity - net_stressed_outflow, 2),
        }
