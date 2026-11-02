"""AEGIS Forward-Looking Enterprise Risk Escalation Forecaster
Predicts the likelihood of risks transitioning from medium to critical over upcoming quarters.
"""
from typing import List, Dict, Any
import numpy as np

class RiskEscalationForecaster:
    @staticmethod
    def forecast_risk_trend(
        current_risk_score: float,
        volatility_index: float,
        external_headwinds_factor: float = 1.15,
        horizon_months: int = 6,
    ) -> Dict[str, Any]:
        """Projects risk index trajectory with compounding volatility."""
        scores = []
        score = current_risk_score

        for m in range(1, horizon_months + 1):
            # Compound risk drift
            drift = (volatility_index * 0.5) * external_headwinds_factor
            score = min(100.0, max(0.0, score + drift))
            scores.append(round(score, 1))

        return {
            "initial_score": current_risk_score,
            "projected_scores": scores,
            "escalation_detected": bool(scores[-1] > 75.0 and current_risk_score <= 75.0),
            "max_projected_risk": max(scores) if scores else current_risk_score,
        }
