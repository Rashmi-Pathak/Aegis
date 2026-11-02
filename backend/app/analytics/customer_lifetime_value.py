"""AEGIS BG/NBD & Gamma-Gamma Customer Lifetime Value (CLV) Engine
Models repeat transaction rates, account drop-out probabilities, and monetary spend expectations.
"""
from typing import Dict, Any, List
import numpy as np

class BGNBDCLVModel:
    @staticmethod
    def expected_transactions_p_alive(
        frequency: int,
        recency: float,
        T_cal: float,
        r: float = 0.24,
        alpha: float = 4.41,
        a: float = 0.05,
        b: float = 0.25,
    ) -> Dict[str, float]:
        """Calculates P(Alive) and expected future transactions over horizon t."""
        # Fader & Hardie BG/NBD probability of customer still being active
        x = frequency
        t_x = recency

        denom = 1.0 + (x > 0) * (a / (b + x - 1.0)) * ((alpha + T_cal) / (alpha + t_x)) ** (r + x)
        p_alive = 1.0 / denom if denom > 0 else 0.5

        # Expected transactions in next 12 periods
        future_t = 12.0
        exp_txns = ((r + x) / (alpha + T_cal)) * future_t * p_alive

        return {
            "probability_customer_alive": round(float(p_alive), 3),
            "expected_12m_transactions": round(float(exp_txns), 2),
            "account_health": "Active & Loyal" if p_alive > 0.75 else ("At-Risk" if p_alive > 0.40 else "Dormant / Lost"),
        }
