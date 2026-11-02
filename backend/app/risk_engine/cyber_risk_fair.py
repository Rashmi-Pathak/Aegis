"""AEGIS Factor Analysis of Information Risk (FAIR) Cyber Exposure Engine
Models Loss Event Frequency (LEF) and Loss Magnitude (LM) across ransomware and data breach risks.
"""
from typing import Dict, Any, List
import numpy as np

class FAIRLossModel:
    @staticmethod
    def simulate_cyber_annual_loss_exposure(
        threat_event_frequency_lambda: float = 2.5,
        vulnerability_pct: float = 18.0,
        loss_magnitude_lognorm_mean: float = 12.5,
        loss_magnitude_lognorm_std: float = 1.2,
        n_trials: int = 5000,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Runs FAIR Monte Carlo simulation: Annual Loss Exposure = LEF * LM."""
        np.random.seed(seed)

        # Threat events ~ Poisson
        threat_events = np.random.poisson(threat_event_frequency_lambda, n_trials)
        # Vulnerability gating
        v_prob = vulnerability_pct / 100.0

        annual_losses = []
        for t_events in threat_events:
            actual_breaches = np.random.binomial(t_events, v_prob)
            if actual_breaches == 0:
                annual_losses.append(0.0)
            else:
                mags = np.random.lognormal(loss_magnitude_lognorm_mean, loss_magnitude_lognorm_std, actual_breaches)
                annual_losses.append(float(np.sum(mags)))

        arr = np.array(annual_losses)

        return {
            "mean_annual_loss_exposure": round(float(np.mean(arr)), 2),
            "p90_worst_case_exposure": round(float(np.percentile(arr, 90)), 2),
            "p99_tail_risk_exposure": round(float(np.percentile(arr, 99)), 2),
            "probability_of_zero_loss_pct": round(float(np.mean(arr == 0)) * 100.0, 1),
            "fair_risk_rating": "Critical Capital Drag" if np.mean(arr) > 1000000.0 else "Insurable Operational Risk",
        }
