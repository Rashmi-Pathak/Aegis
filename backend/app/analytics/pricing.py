"""AEGIS Price Elasticity & Revenue Yield Optimization
Estimates price elasticity of demand (PED), optimal pricing curves, and discount margin erosion.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import scipy.stats as stats


class PricingAnalytics:
    """Quantitative pricing elasticity, margin yield, and demand curve estimation."""

    @staticmethod
    def estimate_price_elasticity(
        prices: List[float],
        quantities: List[float],
    ) -> Dict[str, Any]:
        """Calculates point and arc price elasticity of demand via log-log regression:
        ln(Q) = alpha + beta * ln(P)
        Elasticity = beta
        """
        p = np.array(prices, dtype=float)
        q = np.array(quantities, dtype=float)

        mask = (p > 0) & (q > 0)
        p_clean = p[mask]
        q_clean = q[mask]

        if len(p_clean) < 5:
            return {"elasticity": -1.0, "classification": "Unitary Elastic", "r_squared": 0.0}

        log_p = np.log(p_clean)
        log_q = np.log(q_clean)

        slope, intercept, r_value, p_value, std_err = stats.linregress(log_p, log_q)
        elasticity = round(float(slope), 3)

        if abs(elasticity) > 1.2:
            classification = "Elastic Demand (Price Sensitive)"
        elif abs(elasticity) < 0.8:
            classification = "Inelastic Demand (Strong Pricing Power)"
        else:
            classification = "Unitary Elastic Demand"

        return {
            "elasticity": elasticity,
            "classification": classification,
            "r_squared": round(float(r_value ** 2), 3),
            "p_value": round(float(p_value), 5),
            "standard_error": round(float(std_err), 3),
            "pricing_power_index": round(max(0.0, min(100.0, (1.0 / abs(elasticity)) * 50.0)), 1),
        }

    @staticmethod
    def optimize_price_point(
        marginal_cost: float,
        elasticity: float,
    ) -> Dict[str, float]:
        """Optimal markup formula: P* = MarginalCost * (Elasticity / (1 + Elasticity))."""
        if elasticity >= -1.0:
            # Inelastic or upward-sloping: theoretically infinite pricing power or unbounded
            optimal_p = marginal_cost * 1.50
        else:
            optimal_p = marginal_cost * (abs(elasticity) / (abs(elasticity) - 1.0))

        gross_margin = ((optimal_p - marginal_cost) / optimal_p) * 100.0 if optimal_p > 0 else 0.0

        return {
            "marginal_cost": round(marginal_cost, 2),
            "estimated_elasticity": round(elasticity, 3),
            "optimal_recommended_price": round(optimal_p, 2),
            "implied_optimal_gross_margin_pct": round(gross_margin, 2),
        }
