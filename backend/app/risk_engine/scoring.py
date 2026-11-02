"""AEGIS Quantitative Enterprise Risk Scoring Engine
Combines Bayesian prior probabilities, financial severity loss distributions,
velocity of onset, and internal control detectability into unified risk indexes.
"""

from typing import Dict, Any, List
import numpy as np


class RiskScorer:
    """Enterprise Risk Management (ERM) scoring model calibrated to ISO 31000 & COSO."""

    @staticmethod
    def calculate_risk_score(
        probability: float,  # 0.0 to 1.0
        financial_impact_score: float,  # 0 to 100
        velocity_multiplier: float = 1.0,  # 0.8 (slow) to 1.5 (instant shock)
        detectability_discount: float = 0.9,  # 0.5 (easily caught) to 1.0 (undetected)
    ) -> Dict[str, Any]:
        """Calculates normalized composite risk score (0 to 100) and severity classification."""
        prob_bounded = max(0.01, min(1.0, probability))
        raw_score = prob_bounded * financial_impact_score * velocity_multiplier * detectability_discount
        score = min(100.0, max(0.0, raw_score))

        if score >= 75.0:
            severity = "critical"
            urgency = "Immediate Board / C-Level Mitigation"
        elif score >= 50.0:
            severity = "high"
            urgency = "Weekly Executive Review"
        elif score >= 25.0:
            severity = "medium"
            urgency = "Operational Workgroup Remediation"
        else:
            severity = "low"
            urgency = "Standard Telemetry Monitoring"

        return {
            "risk_score": round(score, 1),
            "severity": severity,
            "action_urgency": urgency,
            "probability": round(prob_bounded, 3),
            "financial_impact_score": round(financial_impact_score, 1),
            "velocity_factor": velocity_multiplier,
        }

    @staticmethod
    def rank_risks(risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sorts risks by composite risk score descending."""
        return sorted(risks, key=lambda x: x.get("risk_score", x.get("score", 0)), reverse=True)
