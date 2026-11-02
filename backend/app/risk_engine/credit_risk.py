"""AEGIS Counterparty Credit Risk & Merton Structural Default Engine
Calculates Probability of Default (PD), Loss Given Default (LGD), Exposure at Default (EAD),
and Expected Loss (EL) across enterprise client portfolios.
"""

from typing import List, Dict, Any
import numpy as np
import scipy.stats as stats


class CreditRiskEngine:
    """Basel Accord compliant counterparty expected loss and Merton structural modeling."""

    @staticmethod
    def calculate_expected_loss(
        exposure_at_default: float,
        probability_of_default: float,
        loss_given_default: float = 0.45,  # Standard unsecured corporate benchmark: 45%
    ) -> Dict[str, float]:
        """Expected Loss = EAD * PD * LGD"""
        ead = max(0.0, exposure_at_default)
        pd = max(0.0, min(1.0, probability_of_default))
        lgd = max(0.0, min(1.0, loss_given_default))

        expected_loss = ead * pd * lgd

        return {
            "exposure_at_default": round(ead, 2),
            "probability_of_default_pct": round(pd * 100.0, 2),
            "loss_given_default_pct": round(lgd * 100.0, 2),
            "expected_credit_loss": round(expected_loss, 2),
            "credit_risk_provision_rate_pct": round((expected_loss / ead) * 100.0, 3) if ead > 0 else 0.0,
        }

    @staticmethod
    def merton_distance_to_default(
        asset_value: float,
        debt_face_value: float,
        asset_volatility: float,
        risk_free_rate: float = 0.04,
        time_to_maturity_years: float = 1.0,
    ) -> Dict[str, float]:
        """Merton (1974) Structural Model:
        d2 = [ln(V / D) + (r - 0.5 * sigma^2) * T] / (sigma * sqrt(T))
        PD = N(-d2)
        """
        if asset_value <= 0 or debt_face_value <= 0 or asset_volatility <= 0:
            return {"distance_to_default": 0.0, "structural_pd_pct": 100.0}

        v = asset_value
        d = debt_face_value
        sigma = asset_volatility
        t = time_to_maturity_years
        r = risk_free_rate

        d1 = (np.log(v / d) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - (sigma * np.sqrt(t))

        pd = float(stats.norm.cdf(-d2))

        return {
            "distance_to_default_sigmas": round(float(d2), 2),
            "structural_probability_of_default_pct": round(pd * 100.0, 3),
            "solvency_cushion_ratio": round(v / d, 2),
        }
