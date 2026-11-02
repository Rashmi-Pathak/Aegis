"""AEGIS Credit Rating Migration & Absorbing Markov Default Chain
Models corporate rating migration probabilities across AAA through Default (D).
"""
from typing import List, Dict, Any
import numpy as np

class CreditTransitionMatrixEngine:
    RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Default"]

    DEFAULT_1Y_TRANSITION = np.array([
        [0.908, 0.083, 0.007, 0.001, 0.001, 0.000, 0.000, 0.000],  # AAA
        [0.006, 0.914, 0.073, 0.005, 0.001, 0.001, 0.000, 0.000],  # AA
        [0.001, 0.021, 0.912, 0.058, 0.005, 0.002, 0.001, 0.000],  # A
        [0.000, 0.002, 0.041, 0.893, 0.048, 0.010, 0.004, 0.002],  # BBB
        [0.000, 0.001, 0.004, 0.063, 0.832, 0.076, 0.014, 0.010],  # BB
        [0.000, 0.001, 0.001, 0.004, 0.068, 0.824, 0.058, 0.044],  # B
        [0.000, 0.000, 0.001, 0.003, 0.015, 0.118, 0.638, 0.225],  # CCC
        [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 1.000],  # Default (Absorbing)
    ])

    @classmethod
    def project_n_year_default_probability(
        cls,
        initial_rating: str,
        n_years: int = 3,
    ) -> Dict[str, Any]:
        """Calculates multi-year rating distribution by powering Markov matrix P^n."""
        if initial_rating not in cls.RATINGS:
            initial_rating = "BBB"

        r_idx = cls.RATINGS.index(initial_rating)

        # Matrix power
        p_n = np.linalg.matrix_power(cls.DEFAULT_1Y_TRANSITION, n_years)
        distribution = p_n[r_idx, :]

        return {
            "initial_rating": initial_rating,
            "projection_horizon_years": n_years,
            "cumulative_default_probability_pct": round(float(distribution[-1]) * 100.0, 3),
            "projected_rating_probabilities": {
                cls.RATINGS[i]: round(float(distribution[i]) * 100.0, 2)
                for i in range(len(cls.RATINGS))
            },
        }
