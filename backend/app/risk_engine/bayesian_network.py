"""AEGIS Bayesian Risk Network & Belief Updating Engine
Updates posterior disruption probabilities conditioned on real-time sensor & telemetry evidence.
"""

from typing import Dict, Any, List


class BayesianRiskUpdater:
    """Calculates posterior risk probabilities P(Disruption | Evidence) via Bayes Theorem."""

    @staticmethod
    def update_posterior_probability(
        prior_probability: float,  # P(Risk)
        evidence_likelihood_given_risk: float,  # P(Evidence | Risk)
        evidence_likelihood_given_normal: float,  # P(Evidence | Normal)
    ) -> Dict[str, float]:
        """P(Risk | Evidence) = [P(Evidence|Risk) * P(Risk)] / P(Evidence)"""
        prior_risk = max(1e-4, min(1.0 - 1e-4, prior_probability))
        prior_normal = 1.0 - prior_risk

        p_evidence = (evidence_likelihood_given_risk * prior_risk) + (
            evidence_likelihood_given_normal * prior_normal
        )

        if p_evidence <= 0:
            posterior = prior_risk
        else:
            posterior = (evidence_likelihood_given_risk * prior_risk) / p_evidence

        bayes_factor = (
            evidence_likelihood_given_risk / evidence_likelihood_given_normal
            if evidence_likelihood_given_normal > 0
            else 999.0
        )

        return {
            "prior_probability": round(prior_risk, 4),
            "posterior_probability": round(float(posterior), 4),
            "bayes_factor": round(float(bayes_factor), 2),
            "probability_shift_pct": round(float((posterior - prior_risk) * 100.0), 2),
        }
