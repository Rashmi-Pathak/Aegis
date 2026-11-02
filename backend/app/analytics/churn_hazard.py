"""AEGIS Cox Proportional Hazards & Semi-Parametric Churn Regression
Estimates hazard ratios h(t) = h_0(t) * exp(beta * X) for enterprise accounts.
"""
from typing import List, Dict, Any
import numpy as np

class CoxHazardEstimator:
    @staticmethod
    def calculate_hazard_ratios(
        feature_names: List[str],
        coefficients: List[float],
    ) -> List[Dict[str, Any]]:
        """Computes Hazard Ratios HR = exp(beta) and interprets risk multiplier."""
        results = []
        for name, beta in zip(feature_names, coefficients):
            hr = float(np.exp(beta))
            pct_change = (hr - 1.0) * 100.0

            if hr > 1.25:
                impact = f"+{pct_change:.1f}% Churn Hazard Risk Surge"
            elif hr < 0.80:
                impact = f"{pct_change:.1f}% Protective / Retention Anchor"
            else:
                impact = "Marginal Risk Effect"

            results.append({
                "covariate": name,
                "beta_coefficient": round(beta, 3),
                "hazard_ratio": round(hr, 3),
                "churn_risk_effect": impact,
            })
        return results
