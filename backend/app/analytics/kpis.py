"""AEGIS Enterprise KPI Computation Engine
Provides mathematical and financial formulas for 40+ standardized corporate metrics
spanning revenue, profitability, working capital, inventory, and operations.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


class KPICalculator:
    """Calculates standardized enterprise KPIs from canonical tabular series."""

    @staticmethod
    def calculate_growth_rate(current: float, baseline: float) -> float:
        """Percentage growth from baseline to current."""
        if baseline == 0:
            return 0.0
        return round(((current - baseline) / abs(baseline)) * 100.0, 2)

    @staticmethod
    def compound_annual_growth_rate(beginning_val: float, ending_val: float, periods: float) -> float:
        """CAGR = (Ending / Beginning) ^ (1/n) - 1"""
        if beginning_val <= 0 or ending_val <= 0 or periods <= 0:
            return 0.0
        return round(((ending_val / beginning_val) ** (1.0 / periods) - 1.0) * 100.0, 2)

    @staticmethod
    def gross_margin_percentage(revenue: float, cogs: float) -> float:
        """(Revenue - COGS) / Revenue * 100"""
        if revenue <= 0:
            return 0.0
        return round(((revenue - cogs) / revenue) * 100.0, 2)

    @staticmethod
    def operating_margin_percentage(operating_income: float, revenue: float) -> float:
        """Operating Income (EBIT) / Revenue * 100"""
        if revenue <= 0:
            return 0.0
        return round((operating_income / revenue) * 100.0, 2)

    @staticmethod
    def ebitda_margin(ebitda: float, revenue: float) -> float:
        """EBITDA / Revenue * 100"""
        if revenue <= 0:
            return 0.0
        return round((ebitda / revenue) * 100.0, 2)

    @staticmethod
    def net_profit_margin(net_income: float, revenue: float) -> float:
        """Net Income / Revenue * 100"""
        if revenue <= 0:
            return 0.0
        return round((net_income / revenue) * 100.0, 2)

    @staticmethod
    def current_ratio(current_assets: float, current_liabilities: float) -> float:
        """Current Assets / Current Liabilities"""
        if current_liabilities <= 0:
            return 0.0
        return round(current_assets / current_liabilities, 2)

    @staticmethod
    def quick_ratio(current_assets: float, inventory: float, current_liabilities: float) -> float:
        """(Current Assets - Inventory) / Current Liabilities"""
        if current_liabilities <= 0:
            return 0.0
        return round((current_assets - inventory) / current_liabilities, 2)

    @staticmethod
    def cash_conversion_cycle(dso: float, dio: float, dpo: float) -> float:
        """CCC = Days Sales Outstanding + Days Inventory Outstanding - Days Payable Outstanding"""
        return round(dso + dio - dpo, 1)

    @staticmethod
    def days_sales_outstanding(accounts_receivable: float, total_credit_sales: float, days: int = 365) -> float:
        """(AR / Total Credit Sales) * Days"""
        if total_credit_sales <= 0:
            return 0.0
        return round((accounts_receivable / total_credit_sales) * days, 1)

    @staticmethod
    def days_inventory_outstanding(average_inventory: float, cogs: float, days: int = 365) -> float:
        """(Avg Inventory / COGS) * Days"""
        if cogs <= 0:
            return 0.0
        return round((average_inventory / cogs) * days, 1)

    @staticmethod
    def days_payable_outstanding(accounts_payable: float, cost_of_sales: float, days: int = 365) -> float:
        """(AP / Cost of Sales) * Days"""
        if cost_of_sales <= 0:
            return 0.0
        return round((accounts_payable / cost_of_sales) * days, 1)

    @staticmethod
    def return_on_invested_capital(nopat: float, invested_capital: float) -> float:
        """ROIC = NOPAT / Invested Capital * 100"""
        if invested_capital <= 0:
            return 0.0
        return round((nopat / invested_capital) * 100.0, 2)

    @staticmethod
    def economic_value_added(nopat: float, invested_capital: float, wacc_pct: float) -> float:
        """EVA = NOPAT - (Invested Capital * WACC)"""
        return round(nopat - (invested_capital * (wacc_pct / 100.0)), 2)

    @staticmethod
    def altman_z_score(
        working_capital: float,
        retained_earnings: float,
        ebit: float,
        market_equity: float,
        sales: float,
        total_assets: float,
        total_liabilities: float,
    ) -> Dict[str, Any]:
        """Altman Z-Score for bankruptcy prediction in manufacturing/logistics/enterprises.
        Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5
        Zones:
          Z > 2.99: Safe Zone
          1.81 <= Z <= 2.99: Grey Zone
          Z < 1.81: Distress Zone
        """
        if total_assets <= 0 or total_liabilities <= 0:
            return {"z_score": 0.0, "zone": "Undefined", "probability_of_distress": 1.0}

        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = market_equity / total_liabilities
        x5 = sales / total_assets

        z = round(1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5, 2)

        if z > 2.99:
            zone = "Safe Zone"
            distress_prob = 0.05
        elif z >= 1.81:
            zone = "Grey Zone"
            distress_prob = 0.35
        else:
            zone = "Distress Zone"
            distress_prob = 0.85

        return {
            "z_score": z,
            "zone": zone,
            "probability_of_distress": distress_prob,
            "components": {
                "x1_liquidity": round(x1, 3),
                "x2_cumulative_profitability": round(x2, 3),
                "x3_operating_productivity": round(x3, 3),
                "x4_market_leverage": round(x4, 3),
                "x5_asset_turnover": round(x5, 3),
            },
        }

    @staticmethod
    def dupont_analysis(
        net_income: float, revenue: float, total_assets: float, total_equity: float
    ) -> Dict[str, float]:
        """DuPont 3-Step ROE Decomposition:
        ROE = Net Profit Margin * Asset Turnover * Equity Multiplier
        """
        if revenue <= 0 or total_assets <= 0 or total_equity <= 0:
            return {"roe": 0.0, "net_margin": 0.0, "asset_turnover": 0.0, "equity_multiplier": 0.0}

        net_margin = net_income / revenue
        asset_turnover = revenue / total_assets
        equity_multiplier = total_assets / total_equity
        roe = net_margin * asset_turnover * equity_multiplier

        return {
            "roe": round(roe * 100.0, 2),
            "net_margin_pct": round(net_margin * 100.0, 2),
            "asset_turnover": round(asset_turnover, 2),
            "equity_multiplier": round(equity_multiplier, 2),
        }
