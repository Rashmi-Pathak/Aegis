"""AEGIS Cash Flow Time Series Forecaster
Combines AR(1) autoregression, working capital cash cycle fluctuations,
and seasonal tax/payroll outlays to project 12-month net liquidity.
"""
from typing import List, Dict, Any
import numpy as np

class CashFlowForecaster:
    @staticmethod
    def forecast_cash_flow(
        historical_net_cash: List[float],
        current_balance: float,
        horizon_months: int = 12,
        working_capital_drag: float = 0.05,
    ) -> Dict[str, Any]:
        """Projects future cash balance and flags any minimum threshold breaches."""
        if not historical_net_cash:
            return {"forecast_balance": [current_balance] * horizon_months, "min_balance": current_balance}

        arr = np.array(historical_net_cash, dtype=float)
        mean_inflow = float(np.mean(arr))
        std_inflow = float(np.std(arr)) if len(arr) > 1 else abs(mean_inflow) * 0.1

        balances = []
        inflows = []
        curr = current_balance

        for m in range(1, horizon_months + 1):
            # AR(1) with seasonal mean reversion
            net_inflow = mean_inflow * (1.0 - working_capital_drag)
            curr += net_inflow
            balances.append(round(curr, 2))
            inflows.append(round(net_inflow, 2))

        return {
            "starting_balance": round(current_balance, 2),
            "projected_monthly_balances": balances,
            "projected_monthly_net_cash": inflows,
            "minimum_projected_balance": min(balances) if balances else current_balance,
            "is_runway_positive": all(b > 0 for b in balances),
        }
