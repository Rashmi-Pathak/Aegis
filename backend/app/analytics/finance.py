"""AEGIS Financial Health & Capital Structure Analytics
Computes working capital dynamics, EBITDA bridges, leverage ratios, and liquidity buffers.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


class FinancialAnalytics:
    """Enterprise balance sheet, income statement, and cash flow diagnostic modeling."""

    @staticmethod
    def compute_ebitda_bridge(
        baseline_ebitda: float,
        price_volume_impact: float,
        cost_inflation_impact: float,
        operational_efficiency_impact: float,
        overhead_variance: float,
    ) -> Dict[str, Any]:
        """Generates an EBITDA waterfall variance bridge from baseline to actual."""
        final_ebitda = (
            baseline_ebitda
            + price_volume_impact
            - cost_inflation_impact
            + operational_efficiency_impact
            - overhead_variance
        )

        steps = [
            {"label": "Baseline EBITDA", "amount": round(baseline_ebitda, 2), "type": "baseline"},
            {"label": "Price / Volume Mix", "amount": round(price_volume_impact, 2), "type": "positive" if price_volume_impact >= 0 else "negative"},
            {"label": "Input Cost Inflation", "amount": round(-cost_inflation_impact, 2), "type": "negative"},
            {"label": "Efficiency / OpEx Gains", "amount": round(operational_efficiency_impact, 2), "type": "positive"},
            {"label": "Overhead Variance", "amount": round(-overhead_variance, 2), "type": "negative" if overhead_variance >= 0 else "positive"},
            {"label": "Reported EBITDA", "amount": round(final_ebitda, 2), "type": "total"},
        ]

        return {
            "starting_ebitda": round(baseline_ebitda, 2),
            "ending_ebitda": round(final_ebitda, 2),
            "variance": round(final_ebitda - baseline_ebitda, 2),
            "bridge_steps": steps,
        }

    @staticmethod
    def analyze_working_capital_efficiency(
        inventory: float,
        accounts_receivable: float,
        accounts_payable: float,
        revenue: float,
        cogs: float,
    ) -> Dict[str, Any]:
        """Measures Net Working Capital (NWC), NWC to Revenue, and Cash Conversion Velocity."""
        nwc = (accounts_receivable + inventory) - accounts_payable
        nwc_intensity_pct = round((nwc / revenue) * 100.0, 2) if revenue > 0 else 0.0

        dso = round((accounts_receivable / revenue) * 365, 1) if revenue > 0 else 0.0
        dio = round((inventory / cogs) * 365, 1) if cogs > 0 else 0.0
        dpo = round((accounts_payable / cogs) * 365, 1) if cogs > 0 else 0.0
        ccc = round(dso + dio - dpo, 1)

        # Capital drag evaluation
        liquidity_status = "Optimal"
        if ccc > 90.0:
            liquidity_status = "Severe Capital Drag"
        elif ccc > 60.0:
            liquidity_status = "Sub-Optimal Working Capital"
        elif ccc < 20.0:
            liquidity_status = "High Velocity / Negative Working Capital Buffer"

        return {
            "net_working_capital": round(nwc, 2),
            "nwc_revenue_intensity_pct": nwc_intensity_pct,
            "days_sales_outstanding": dso,
            "days_inventory_outstanding": dio,
            "days_payable_outstanding": dpo,
            "cash_conversion_cycle_days": ccc,
            "liquidity_status": liquidity_status,
        }

    @staticmethod
    def debt_service_coverage_ratio(ebitda: float, capex: float, principal_repayment: float, interest_expense: float) -> float:
        """DSCR = (EBITDA - CapEx) / (Principal + Interest)
        Standard Covenant Threshold: >= 1.25x
        """
        debt_service = principal_repayment + interest_expense
        if debt_service <= 0:
            return 999.0
        return round((ebitda - capex) / debt_service, 2)
