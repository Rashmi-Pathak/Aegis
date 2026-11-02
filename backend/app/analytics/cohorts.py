"""AEGIS Enterprise Customer & Contract Cohort Analytics
Computes longitudinal cohort retention curves, Kaplan-Meier churn survival functions,
and hazard rates across annual and monthly customer vintages.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd


class CohortAnalytics:
    """Longitudinal cohort survival analysis and customer churn hazard modeling."""

    @staticmethod
    def kaplan_meier_survival(
        durations: List[float],
        event_observed: List[bool],
    ) -> Dict[str, Any]:
        """Calculates Kaplan-Meier product-limit survival estimates:
        S(t) = Product_{t_i <= t} (1 - d_i / n_i)
        """
        if not durations or not event_observed or len(durations) != len(event_observed):
            return {"timeline": [], "survival_probabilities": [], "median_survival_time": 0.0}

        df = pd.DataFrame({"duration": durations, "event": event_observed})
        df = df.sort_values(by="duration")

        unique_times = np.sort(df["duration"].unique())
        n_at_risk = len(df)
        survival_prob = 1.0

        timeline = []
        survival_probabilities = []
        hazard_rates = []

        for t in unique_times:
            sub = df[df["duration"] == t]
            d_i = sub["event"].sum()  # Churned events at time t
            w_i = len(sub) - d_i      # Censored accounts at time t

            if n_at_risk > 0:
                step_survival = (1.0 - (d_i / n_at_risk))
                survival_prob *= step_survival
                hazard = d_i / n_at_risk
            else:
                step_survival = 0.0
                hazard = 0.0

            timeline.append(float(t))
            survival_probabilities.append(round(float(survival_prob), 4))
            hazard_rates.append(round(float(hazard), 4))

            n_at_risk -= (d_i + w_i)

        # Median survival time is when S(t) <= 0.50
        median_time = float(unique_times[-1]) if len(unique_times) > 0 else 0.0
        for t, s in zip(timeline, survival_probabilities):
            if s <= 0.50:
                median_time = t
                break

        return {
            "timeline_periods": timeline,
            "survival_probabilities": survival_probabilities,
            "hazard_rates": hazard_rates,
            "median_survival_time": median_time,
            "retention_at_12_periods": survival_probabilities[min(11, len(survival_probabilities) - 1)] if survival_probabilities else 1.0,
        }

    @staticmethod
    def calculate_nrr_matrix(
        cohort_rev_df: pd.DataFrame,
    ) -> List[Dict[str, Any]]:
        """Calculates Net Revenue Retention (NRR) expansion and contraction per cohort."""
        matrix = []
        for cohort_id, group in cohort_rev_df.groupby("cohort"):
            sorted_g = group.sort_values("period")
            base = sorted_g.iloc[0]["revenue"] if not sorted_g.empty else 1.0
            row = {"cohort": str(cohort_id), "base_revenue": float(base), "periods": {}}
            for _, r in sorted_g.iterrows():
                p = int(r["period"])
                rev = float(r["revenue"])
                row["periods"][f"P{p}"] = round((rev / base) * 100.0, 1) if base > 0 else 0.0
            matrix.append(row)
        return matrix
