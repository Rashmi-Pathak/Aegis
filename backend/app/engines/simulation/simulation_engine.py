from typing import Dict, Any
from app.schemas.simulation import SimulationParams, SimulationResult

class WhatIfSimulationEngine:
    """Isolated, non-destructive counterfactual business simulation engine."""

    BASELINE_REVENUE = 148.24
    BASELINE_PROFIT = 21.05
    BASELINE_CASH = 18.65
    BASELINE_RISK = 74

    @classmethod
    def run_simulation(cls, params: SimulationParams) -> SimulationResult:
        """Project simulated metrics against baseline snapshots without modifying production records."""
        # Sensitivity coefficients
        rev_multiplier = 1.0 + (params.marketingSpendDelta * 0.45 + params.priceDelta * 0.85) / 100.0
        profit_multiplier = 1.0 + (params.priceDelta * 1.25 - params.marketingSpendDelta * 0.22 - params.procurementDelta * 0.42) / 100.0
        cash_multiplier = 1.0 + (params.priceDelta * 0.15 - params.inventoryBufferDelta * 0.35) / 100.0
        risk_delta = (params.marketingSpendDelta * 0.15 + params.procurementDelta * 0.38 - params.inventoryBufferDelta * 0.42 - params.priceDelta * 0.5)

        sim_rev = round(cls.BASELINE_REVENUE * rev_multiplier, 2)
        sim_profit = round(cls.BASELINE_PROFIT * profit_multiplier, 2)
        sim_cash = round(cls.BASELINE_CASH * cash_multiplier, 2)
        sim_risk = int(max(15, min(95, round(cls.BASELINE_RISK + risk_delta))))

        tradeoffs = [
            f"Price adjustment of {'+' if params.priceDelta >= 0 else ''}{params.priceDelta}% yields ${sim_profit}M projected net margin"
            if params.priceDelta != 0 else "Pricing baseline maintained with zero volume friction",
            f"Marketing spend delta of {'+' if params.marketingSpendDelta >= 0 else ''}{params.marketingSpendDelta}% balances customer acquisition rate"
            if params.marketingSpendDelta != 0 else "Customer acquisition channel spend steady",
            f"Inventory safety buffer of {'+' if params.inventoryBufferDelta >= 0 else ''}{params.inventoryBufferDelta}% modifies stockout protection"
            if params.inventoryBufferDelta != 0 else "Inventory carrying costs stable",
        ]

        return SimulationResult(
            baselineRevenue=cls.BASELINE_REVENUE,
            simulatedRevenue=sim_rev,
            baselineProfit=cls.BASELINE_PROFIT,
            simulatedProfit=sim_profit,
            baselineCashFlow=cls.BASELINE_CASH,
            simulatedCashFlow=sim_cash,
            baselineRiskScore=cls.BASELINE_RISK,
            simulatedRiskScore=sim_risk,
            tradeoffs=tradeoffs,
        )
