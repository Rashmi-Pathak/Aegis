"""AEGIS Data Drift & Covariate Shift Diagnostics
Calculates Population Stability Index (PSI) and Kolmogorov-Smirnov drift tests.
"""

from typing import Dict, Any, List, Union
import numpy as np
import scipy.stats as stats


class DataDriftDetector:
    """Measures distributional drift between baseline training telemetry and live batches."""

    @staticmethod
    def calculate_psi(
        baseline: Union[List[float], np.ndarray],
        target: Union[List[float], np.ndarray],
        num_buckets: int = 10,
    ) -> Dict[str, Any]:
        """Population Stability Index (PSI).
        PSI < 0.1: No significant drift.
        0.1 <= PSI <= 0.25: Moderate drift, requires monitoring.
        PSI > 0.25: Significant drift, model retraining mandatory.
        """
        b = np.array(baseline, dtype=float)
        t = np.array(target, dtype=float)

        b = b[~np.isnan(b)]
        t = t[~np.isnan(t)]

        if len(b) < 10 or len(t) < 10:
            return {"psi": 0.0, "drift_detected": False, "status": "Insufficient Sample"}

        # Define bin edges on baseline
        percentiles = np.linspace(0, 100, num_buckets + 1)
        bin_edges = np.percentile(b, percentiles)
        bin_edges[0] -= 1e-5
        bin_edges[-1] += 1e-5

        # Count frequencies
        b_counts, _ = np.histogram(b, bins=bin_edges)
        t_counts, _ = np.histogram(t, bins=bin_edges)

        # Smooth zero counts
        b_pct = (b_counts + 1e-4) / (len(b) + 1e-4 * num_buckets)
        t_pct = (t_counts + 1e-4) / (len(t) + 1e-4 * num_buckets)

        psi_val = np.sum((t_pct - b_pct) * np.log(t_pct / b_pct))
        psi_score = round(float(psi_val), 4)

        drift = bool(psi_score > 0.20)
        status = "Severe Drift" if psi_score > 0.25 else ("Moderate Drift" if psi_score >= 0.10 else "Stable")

        return {
            "psi": psi_score,
            "drift_detected": drift,
            "drift_status": status,
            "baseline_samples": len(b),
            "target_samples": len(t),
        }

    @staticmethod
    def kolmogorov_smirnov_test(
        baseline: Union[List[float], np.ndarray],
        target: Union[List[float], np.ndarray],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        """Two-sample Kolmogorov-Smirnov test for continuous distributions."""
        b = np.array(baseline, dtype=float)
        t = np.array(target, dtype=float)

        statistic, p_value = stats.ks_2samp(b[~np.isnan(b)], t[~np.isnan(t)])

        return {
            "ks_statistic": round(float(statistic), 4),
            "p_value": round(float(p_value), 5),
            "drift_detected": bool(p_value < alpha),
        }
