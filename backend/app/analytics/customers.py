"""AEGIS Customer Analytics & Risk Scoring Engine
Implements RFM (Recency, Frequency, Monetary) segmentation, customer churn probability,
and revenue concentration risk modeling.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


class CustomerAnalytics:
    """Customer portfolio risk, RFM segmentation, and concentration analysis."""

    @staticmethod
    def calculate_rfm_scores(
        transactions_df: pd.DataFrame,
        customer_id_col: str = "customer_id",
        date_col: str = "date",
        amount_col: str = "amount",
        reference_date: Optional[pd.Timestamp] = None,
    ) -> List[Dict[str, Any]]:
        """Computes RFM quantiles and segments customers into operational cohorts."""
        if transactions_df.empty:
            return []

        df = transactions_df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[customer_id_col, date_col, amount_col])

        if df.empty:
            return []

        ref = reference_date or (df[date_col].max() + pd.Timedelta(days=1))

        rfm = df.groupby(customer_id_col).agg(
            recency=(date_col, lambda x: (ref - x.max()).days),
            frequency=(date_col, "count"),
            monetary=(amount_col, "sum"),
        ).reset_index()

        # Quantile scoring 1-5
        for col, ascending in [("recency", False), ("frequency", True), ("monetary", True)]:
            try:
                rfm[f"{col[0]}_score"] = pd.qcut(
                    rfm[col].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
                ).astype(int)
            except Exception:
                rfm[f"{col[0]}_score"] = 3

        def assign_segment(row):
            r, f, m = row["r_score"], row["f_score"], row["m_score"]
            if r >= 4 and f >= 4 and m >= 4:
                return "Enterprise Champions"
            elif r >= 3 and f >= 3:
                return "Loyal Core Accounts"
            elif r >= 4 and f <= 2:
                return "Recent Inflow"
            elif r <= 2 and f >= 3:
                return "At-Risk High Volume"
            elif r == 1:
                return "Severe Churn Risk"
            else:
                return "Mid-Tier Base"

        rfm["segment"] = rfm.apply(assign_segment, axis=1)

        result = []
        for _, row in rfm.head(50).iterrows():
            result.append({
                "customerId": str(row[customer_id_col]),
                "recencyDays": int(row["recency"]),
                "frequencyOrders": int(row["frequency"]),
                "monetaryValue": round(float(row["monetary"]), 2),
                "rfmScore": f"{row['r_score']}{row['f_score']}{row['m_score']}",
                "segment": row["segment"],
            })

        return result

    @staticmethod
    def calculate_concentration_risk(
        customer_revenues: List[float],
    ) -> Dict[str, Any]:
        """Calculates Herfindahl-Hirschman Index (HHI) and Top-N Revenue Concentration."""
        if not customer_revenues:
            return {"hhi": 0.0, "top_5_pct": 0.0, "top_10_pct": 0.0, "risk_level": "Low"}

        revs = np.array(sorted(customer_revenues, reverse=True))
        total_rev = np.sum(revs)

        if total_rev <= 0:
            return {"hhi": 0.0, "top_5_pct": 0.0, "top_10_pct": 0.0, "risk_level": "Low"}

        shares = (revs / total_rev) * 100.0
        hhi = float(np.sum(shares ** 2))

        top_5_pct = float(np.sum(shares[:5]))
        top_10_pct = float(np.sum(shares[:10]))

        risk_level = "Low"
        if top_5_pct > 60.0 or hhi > 2500:
            risk_level = "Critical Client Dependency"
        elif top_5_pct > 40.0 or hhi > 1500:
            risk_level = "Elevated Concentration"

        return {
            "hhi_index": round(hhi, 1),
            "top_5_revenue_share_pct": round(top_5_pct, 1),
            "top_10_revenue_share_pct": round(top_10_pct, 1),
            "concentration_risk_level": risk_level,
        }
