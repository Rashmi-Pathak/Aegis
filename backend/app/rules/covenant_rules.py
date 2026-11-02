"""AEGIS Debt Covenant & Solvency Policy Rules
Standardized banking and credit agreement covenants (DSCR, Leverage, Minimum Liquidity).
"""

from typing import List, Dict, Any
from app.rules.rule_evaluator import BusinessRuleEvaluator


class CovenantRules:
    """Pre-configured enterprise lending covenant rule definitions."""

    DEFAULT_COVENANTS = [
        {
            "id": "cov_min_dscr",
            "name": "Debt Service Coverage Ratio (DSCR) Floor",
            "field": "debt_service_coverage_ratio",
            "op": "<",
            "threshold": 1.25,
            "severity": "critical",
            "action": "Immediate bank waiver notification & CapEx freeze required.",
        },
        {
            "id": "cov_max_leverage",
            "name": "Net Debt to EBITDA Ceiling",
            "field": "net_debt_to_ebitda",
            "op": ">",
            "threshold": 3.75,
            "severity": "high",
            "action": "Suspend share repurchases & dividend distributions.",
        },
        {
            "id": "cov_min_liquidity",
            "name": "Minimum Available Liquidity Cash Buffer",
            "field": "cash_reserve_usd",
            "op": "<",
            "threshold": 5000000.0,
            "severity": "critical",
            "action": "Draw down revolving credit facility immediately.",
        },
        {
            "id": "cov_min_current_ratio",
            "name": "Current Ratio Liquidity Floor",
            "field": "current_ratio",
            "op": "<",
            "threshold": 1.15,
            "severity": "medium",
            "action": "Accelerate AR collection & defer discretionary supplier payables.",
        },
    ]

    @classmethod
    def audit_covenants(cls, financials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Audits financial metrics against banking covenants."""
        return BusinessRuleEvaluator.evaluate_rule_set(financials, cls.DEFAULT_COVENANTS)
