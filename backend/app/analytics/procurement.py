"""AEGIS Procurement & Supplier Dependency Risk Engine
Classifies enterprise suppliers along the Kraljic Matrix and computes single-source vulnerability scores.
"""

from typing import List, Dict, Any
import numpy as np


class ProcurementAnalytics:
    """Supplier concentration, Kraljic portfolio matrix, and contract exposure modeling."""

    @staticmethod
    def classify_kraljic_matrix(
        suppliers: List[Dict[str, Any]],  # name, annual_spend, supply_risk_score (1-10), substitutability (1-10)
    ) -> List[Dict[str, Any]]:
        """Kraljic Portfolio Matrix:
        - Strategic: High Spend, High Supply Risk
        - Bottleneck: Low Spend, High Supply Risk (Dangerous vulnerability)
        - Leverage: High Spend, Low Supply Risk
        - Non-Critical: Low Spend, Low Supply Risk
        """
        if not suppliers:
            return []

        spends = [s.get("annual_spend", 0.0) for s in suppliers]
        median_spend = float(np.median(spends)) if spends else 100000.0

        categorized = []
        for s in suppliers:
            spend = s.get("annual_spend", 0.0)
            risk = s.get("supply_risk_score", 5.0)

            is_high_spend = spend >= median_spend
            is_high_risk = risk >= 6.0

            if is_high_spend and is_high_risk:
                category = "Strategic Partners (Critical)"
                action = "Close Executive Collaboration & Hedging"
            elif not is_high_spend and is_high_risk:
                category = "Bottleneck Suppliers (High Vulnerability)"
                action = "Secure Safety Buffer & Dual-Sourcing"
            elif is_high_spend and not is_high_risk:
                category = "Leverage Commodities (Cost Focus)"
                action = "Competitive Reverse Auctions"
            else:
                category = "Non-Critical Items"
                action = "Automated Procurement & Consolidation"

            categorized.append({
                **s,
                "kraljic_quadrant": category,
                "mitigation_playbook": action,
                "vulnerability_index": round((spend / sum(spends)) * (risk / 10.0) * 100.0, 2) if sum(spends) > 0 else 0.0,
            })

        return sorted(categorized, key=lambda x: x["vulnerability_index"], reverse=True)
