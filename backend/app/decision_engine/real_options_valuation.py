"""AEGIS Real Options Valuation & Binomial Lattice Engine
Values strategic flexibility: Option to Expand, Option to Defer, Option to Abandon capital projects.
"""
from typing import Dict, Any, List
import numpy as np

class RealOptionsBinomialLattice:
    @staticmethod
    def price_expansion_option(
        underlying_asset_value_S: float,
        expansion_capital_cost_K: float,
        volatility_sigma: float = 0.25,
        risk_free_rate_r: float = 0.05,
        time_to_expiry_years_T: float = 2.0,
        lattice_steps_N: int = 4,
    ) -> Dict[str, Any]:
        """Cox, Ross, Rubinstein (CRR) binomial lattice option pricing."""
        dt = time_to_expiry_years_T / lattice_steps_N
        u = np.exp(volatility_sigma * np.sqrt(dt))
        d = 1.0 / u
        p = (np.exp(risk_free_rate_r * dt) - d) / (u - d)

        # Asset tree at maturity
        asset_values = np.zeros(lattice_steps_N + 1)
        option_values = np.zeros(lattice_steps_N + 1)

        for j in range(lattice_steps_N + 1):
            s_t = underlying_asset_value_S * (u ** (lattice_steps_N - j)) * (d ** j)
            asset_values[j] = s_t
            option_values[j] = max(0.0, s_t - expansion_capital_cost_K)

        # Backward rollback
        disc = np.exp(-risk_free_rate_r * dt)
        for step in range(lattice_steps_N - 1, -1, -1):
            for j in range(step + 1):
                option_values[j] = disc * (p * option_values[j] + (1.0 - p) * option_values[j + 1])

        real_option_val = float(option_values[0])
        expanded_npv = (underlying_asset_value_S - expansion_capital_cost_K) + real_option_val

        return {
            "underlying_project_value": underlying_asset_value_S,
            "strike_capital_cost": expansion_capital_cost_K,
            "real_option_value": round(real_option_val, 2),
            "expanded_strategic_npv": round(expanded_npv, 2),
            "up_factor": round(float(u), 3),
            "down_factor": round(float(d), 3),
            "recommendation": "Maintain Strategic Growth Option" if real_option_val > 0 else "Abandon Expansion",
        }
