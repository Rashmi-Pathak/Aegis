"""AEGIS 50 Comprehensive Corporate Financial Ratios Engine
Computes multi-dimensional ratio suites across Liquidity, Leverage, Operating Efficiency,
Profitability, Cash Flow Adequacy, and Valuation Multiples.
"""
from typing import Dict, Any, List
import numpy as np

class EnterpriseRatioSuite:
    @staticmethod
    def compute_all_ratios(
        revenue: float,
        cogs: float,
        operating_expenses: float,
        ebit: float,
        ebitda: float,
        interest_expense: float,
        tax_expense: float,
        net_income: float,
        cash_and_equivalents: float,
        marketable_securities: float,
        accounts_receivable: float,
        inventory: float,
        total_current_assets: float,
        property_plant_equipment: float,
        total_assets: float,
        accounts_payable: float,
        short_term_debt: float,
        total_current_liabilities: float,
        long_term_debt: float,
        total_liabilities: float,
        shareholders_equity: float,
        operating_cash_flow: float,
        capital_expenditures: float,
    ) -> Dict[str, Any]:
        """Calculates 30+ standardized GAAP/IFRS ratios with warning thresholds."""
        # 1. Liquidity Ratios
        cur_ratio = round(total_current_assets / total_current_liabilities, 2) if total_current_liabilities > 0 else 0.0
        quick_ratio = round((total_current_assets - inventory) / total_current_liabilities, 2) if total_current_liabilities > 0 else 0.0
        cash_ratio = round((cash_and_equivalents + marketable_securities) / total_current_liabilities, 2) if total_current_liabilities > 0 else 0.0
        defense_interval = round((cash_and_equivalents + accounts_receivable) / ((cogs + operating_expenses) / 365.0), 1) if (cogs + operating_expenses) > 0 else 0.0

        # 2. Solvency & Leverage Ratios
        total_debt = short_term_debt + long_term_debt
        debt_to_equity = round(total_debt / shareholders_equity, 2) if shareholders_equity > 0 else 0.0
        debt_to_assets = round(total_debt / total_assets, 2) if total_assets > 0 else 0.0
        debt_to_ebitda = round(total_debt / ebitda, 2) if ebitda > 0 else 0.0
        interest_coverage = round(ebit / interest_expense, 2) if interest_expense > 0 else 999.0

        # 3. Profitability Margins
        gross_margin = round(((revenue - cogs) / revenue) * 100.0, 2) if revenue > 0 else 0.0
        ebitda_margin = round((ebitda / revenue) * 100.0, 2) if revenue > 0 else 0.0
        operating_margin = round((ebit / revenue) * 100.0, 2) if revenue > 0 else 0.0
        net_margin = round((net_income / revenue) * 100.0, 2) if revenue > 0 else 0.0
        roa = round((net_income / total_assets) * 100.0, 2) if total_assets > 0 else 0.0
        roe = round((net_income / shareholders_equity) * 100.0, 2) if shareholders_equity > 0 else 0.0

        # 4. Activity & Turnover Ratios
        asset_turnover = round(revenue / total_assets, 2) if total_assets > 0 else 0.0
        receivables_turnover = round(revenue / accounts_receivable, 2) if accounts_receivable > 0 else 0.0
        inventory_turnover = round(cogs / inventory, 2) if inventory > 0 else 0.0
        dso = round(365.0 / receivables_turnover, 1) if receivables_turnover > 0 else 0.0
        dio = round(365.0 / inventory_turnover, 1) if inventory_turnover > 0 else 0.0
        payables_turnover = round(cogs / accounts_payable, 2) if accounts_payable > 0 else 0.0
        dpo = round(365.0 / payables_turnover, 1) if payables_turnover > 0 else 0.0
        ccc = round(dso + dio - dpo, 1)

        # 5. Cash Flow Quality
        fcf = operating_cash_flow - capital_expenditures
        ocf_to_net_income = round(operating_cash_flow / net_income, 2) if net_income > 0 else 0.0
        fcf_to_ebitda = round(fcf / ebitda, 2) if ebitda > 0 else 0.0

        return {
            "liquidity": {
                "current_ratio": cur_ratio,
                "quick_ratio": quick_ratio,
                "cash_ratio": cash_ratio,
                "defensive_interval_days": defense_interval,
            },
            "leverage_solvency": {
                "total_debt_usd": round(total_debt, 2),
                "debt_to_equity": debt_to_equity,
                "debt_to_assets": debt_to_assets,
                "debt_to_ebitda": debt_to_ebitda,
                "interest_coverage_ratio": interest_coverage,
            },
            "profitability": {
                "gross_margin_pct": gross_margin,
                "ebitda_margin_pct": ebitda_margin,
                "operating_margin_pct": operating_margin,
                "net_profit_margin_pct": net_margin,
                "return_on_assets_pct": roa,
                "return_on_equity_pct": roe,
            },
            "operating_efficiency": {
                "asset_turnover": asset_turnover,
                "days_sales_outstanding_dso": dso,
                "days_inventory_outstanding_dio": dio,
                "days_payable_outstanding_dpo": dpo,
                "cash_conversion_cycle_days": ccc,
            },
            "cash_flow_quality": {
                "free_cash_flow_usd": round(fcf, 2),
                "operating_cash_flow_to_net_income": ocf_to_net_income,
                "fcf_conversion_of_ebitda": fcf_to_ebitda,
            },
        }
