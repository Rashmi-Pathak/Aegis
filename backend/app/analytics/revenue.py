"""AEGIS Revenue & ARR Waterfall Analytics Module
Calculates revenue velocity, cohort retention decays, customer acquisition payback,
and net revenue retention (NRR) matrices.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd


class RevenueAnalytics:
    """Enterprise revenue modeling, cohort retention, and subscription/contract analytics."""

    @staticmethod
    def calculate_arr_waterfall(
        starting_arr: float,
        new_bookings: float,
        expansion_arr: float,
        contraction_arr: float,
        churned_arr: float,
    ) -> Dict[str, Any]:
        """Calculates standard SaaS / Recurring Contract ARR Waterfall.
        Ending ARR = Starting + New + Expansion - Contraction - Churn
        """
        net_new_arr = new_bookings + expansion_arr - contraction_arr - churned_arr
        ending_arr = starting_arr + net_new_arr

        # Net Revenue Retention (NRR) = (Starting + Expansion - Contraction - Churn) / Starting
        nrr = (
            round(((starting_arr + expansion_arr - contraction_arr - churned_arr) / starting_arr) * 100.0, 2)
            if starting_arr > 0
            else 100.0
        )

        # Gross Revenue Retention (GRR) = (Starting - Contraction - Churn) / Starting
        grr = (
            round(((starting_arr - contraction_arr - churned_arr) / starting_arr) * 100.0, 2)
            if starting_arr > 0
            else 100.0
        )

        return {
            "starting_arr": round(starting_arr, 2),
            "new_bookings": round(new_bookings, 2),
            "expansion_arr": round(expansion_arr, 2),
            "contraction_arr": round(contraction_arr, 2),
            "churned_arr": round(churned_arr, 2),
            "net_new_arr": round(net_new_arr, 2),
            "ending_arr": round(ending_arr, 2),
            "net_revenue_retention_pct": nrr,
            "gross_revenue_retention_pct": grr,
            "arr_growth_rate_pct": round((net_new_arr / starting_arr) * 100.0, 2) if starting_arr > 0 else 0.0,
        }

    @staticmethod
    def compute_cohort_revenue_matrix(
        transactions_df: pd.DataFrame,
        customer_id_col: str = "customer_id",
        date_col: str = "date",
        amount_col: str = "amount",
    ) -> Dict[str, Any]:
        """Generates cohort vintage survival curves from transactional ledger."""
        if transactions_df.empty or date_col not in transactions_df.columns:
            return {"cohorts": [], "retention_matrix": []}

        df = transactions_df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col, customer_id_col, amount_col])

        if df.empty:
            return {"cohorts": [], "retention_matrix": []}

        df["order_month"] = df[date_col].dt.to_period("M")
        df["cohort"] = df.groupby(customer_id_col)["order_month"].transform("min")

        df["cohort_index"] = (df["order_month"] - df["cohort"]).apply(lambda x: x.n if hasattr(x, "n") else 0)

        cohort_data = (
            df.groupby(["cohort", "cohort_index"])[amount_col]
            .sum()
            .reset_index()
        )

        cohort_sizes = (
            cohort_data[cohort_data["cohort_index"] == 0]
            .set_index("cohort")[amount_col]
            .to_dict()
        )

        cohort_matrix = []
        for cohort, group in cohort_data.groupby("cohort"):
            base_amt = cohort_sizes.get(cohort, 1.0)
            row = {
                "cohort": str(cohort),
                "initial_revenue": float(base_amt),
                "periods": {},
            }
            for _, r in group.iterrows():
                idx = int(r["cohort_index"])
                rev = float(r[amount_col])
                retention_pct = round((rev / base_amt) * 100.0, 1) if base_amt > 0 else 0.0
                row["periods"][f"M{idx}"] = retention_pct
            cohort_matrix.append(row)

        return {
            "total_cohorts": len(cohort_matrix),
            "retention_matrix": cohort_matrix[:12],  # Return up to 12 recent cohorts
        }

    @staticmethod
    def calculate_ltv_cac_ratio(
        arpu_annual: float,
        gross_margin_pct: float,
        annual_churn_rate_pct: float,
        cac: float,
    ) -> Dict[str, float]:
        """Calculates Customer Lifetime Value (LTV) and LTV:CAC efficiency index.
        LTV = (ARPU * Gross Margin) / Churn Rate
        Healthy Benchmark: LTV / CAC >= 3.0x
        """
        if annual_churn_rate_pct <= 0 or cac <= 0:
            return {"ltv": 0.0, "cac": cac, "ratio": 0.0, "payback_months": 0.0}

        margin_decimal = gross_margin_pct / 100.0
        churn_decimal = annual_churn_rate_pct / 100.0

        ltv = (arpu_annual * margin_decimal) / churn_decimal
        ratio = round(ltv / cac, 2)
        payback_months = round((cac / (arpu_annual * margin_decimal / 12.0)), 1)

        return {
            "customer_lifetime_value": round(ltv, 2),
            "customer_acquisition_cost": round(cac, 2),
            "ltv_to_cac_ratio": ratio,
            "cac_payback_months": payback_months,
            "is_sustainable": bool(ratio >= 3.0 and payback_months <= 18.0),
        }
