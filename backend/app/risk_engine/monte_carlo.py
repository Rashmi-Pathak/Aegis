"""AEGIS Stochastic Monte Carlo Simulation Engine
Runs 10,000 parameter trials across joint probability distributions to forecast
capital outcomes and probability of ruin.
"""

from typing import Dict, Any, List, Optional
import numpy as np


class MonteCarloEngine:
    """Stochastic simulation for enterprise cash flow, revenue risk, and operating margins."""

    @staticmethod
    def simulate_revenue_ebitda(
        baseline_revenue: float,
        baseline_ebitda: float,
        revenue_volatility_pct: float = 8.0,
        cost_inflation_range: tuple = (2.0, 12.0),
        fuel_energy_hike_range: tuple = (5.0, 30.0),
        n_iterations: int = 5000,
        random_seed: int = 42,
    ) -> Dict[str, Any]:
        """Runs multi-factor stochastic simulation of operating income under stress."""
        np.random.seed(random_seed)

        # Revenue fluctuation ~ Normal distribution
        rev_shocks = np.random.normal(
            loc=0.0,
            scale=(revenue_volatility_pct / 100.0),
            size=n_iterations,
        )
        simulated_revenues = baseline_revenue * (1.0 + rev_shocks)

        # Cost inflation ~ Triangular distribution (min, peak, max)
        cost_shocks = np.random.triangular(
            left=(cost_inflation_range[0] / 100.0),
            mode=((cost_inflation_range[0] + cost_inflation_range[1]) / 200.0),
            right=(cost_inflation_range[1] / 100.0),
            size=n_iterations,
        )

        # Fuel energy shock
        energy_shocks = np.random.uniform(
            low=(fuel_energy_hike_range[0] / 100.0),
            high=(fuel_energy_hike_range[1] / 100.0),
            size=n_iterations,
        )

        # Baseline cost base
        baseline_costs = baseline_revenue - baseline_ebitda
        simulated_costs = baseline_costs * (1.0 + (cost_shocks * 0.7) + (energy_shocks * 0.3))

        simulated_ebitda = simulated_revenues - simulated_costs
        simulated_margins = (simulated_ebitda / simulated_revenues) * 100.0

        # Percentile distribution
        p5 = float(np.percentile(simulated_ebitda, 5))
        p25 = float(np.percentile(simulated_ebitda, 25))
        p50 = float(np.percentile(simulated_ebitda, 50))
        p75 = float(np.percentile(simulated_ebitda, 75))
        p95 = float(np.percentile(simulated_ebitda, 95))

        prob_negative_ebitda = float(np.mean(simulated_ebitda < 0)) * 100.0

        return {
            "iterations_run": n_iterations,
            "baseline_ebitda": round(baseline_ebitda, 2),
            "expected_ebitda_p50": round(p50, 2),
            "worst_case_p5": round(p5, 2),
            "best_case_p95": round(p95, 2),
            "interquartile_range": [round(p25, 2), round(p75, 2)],
            "probability_of_negative_ebitda_pct": round(prob_negative_ebitda, 2),
            "mean_simulated_margin_pct": round(float(np.mean(simulated_margins)), 2),
            "min_simulated_margin_pct": round(float(np.min(simulated_margins)), 2),
        }
