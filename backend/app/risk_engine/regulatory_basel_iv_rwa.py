"""AEGIS Basel IV Regulatory Capital & Risk-Weighted Assets (RWA) Engine
Calculates Standardized Approach Risk-Weighted Assets (RWA) and Tier 1 Minimum Capital.
"""
from typing import Dict, Any, List

class BaselIVCapitalEngine:
    RISK_WEIGHTS_BY_RATING = {
        "AAA": 0.20,
        "AA": 0.20,
        "A": 0.50,
        "BBB": 0.75,
        "BB": 1.00,
        "B": 1.50,
        "Unrated": 1.00,
    }

    @classmethod
    def calculate_capital_requirement(
        cls,
        credit_exposures: List[Dict[str, Any]],  # exposure_amount, rating
        operational_loss_historical_mean: float = 2000000.0,
        tier1_capital_target_pct: float = 10.5,
    ) -> Dict[str, Any]:
        """Calculates Credit RWA, Operational RWA, and Required Regulatory Equity Cushion."""
        credit_rwa = 0.0
        for exp in credit_exposures:
            amt = exp.get("exposure_amount", 0.0)
            rating = exp.get("rating", "BBB")
            weight = cls.RISK_WEIGHTS_BY_RATING.get(rating, 1.00)
            credit_rwa += amt * weight

        # Basel SMA Operational Risk RWA approximation (12.5 * Business Indicator Component)
        operational_rwa = operational_loss_historical_mean * 12.5
        total_rwa = credit_rwa + operational_rwa

        required_capital = total_rwa * (tier1_capital_target_pct / 100.0)

        return {
            "credit_rwa_usd": round(credit_rwa, 2),
            "operational_rwa_usd": round(operational_rwa, 2),
            "total_risk_weighted_assets_usd": round(total_rwa, 2),
            "minimum_tier1_capital_required_usd": round(required_capital, 2),
            "target_capital_ratio_pct": tier1_capital_target_pct,
        }
