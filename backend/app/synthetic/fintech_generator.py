"""AEGIS Synthetic Commercial Banking & FinTech Loan Portfolio Generator
Generates commercial credit facilities, debt service ratios, risk ratings, and default migrations.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class CommercialCreditGenerator:
    @classmethod
    def generate_loan_book(
        cls,
        n_borrowers: int = 300,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        industries = ["Logistics", "Manufacturing", "Healthcare", "Hospitality", "Commercial Real Estate"]
        ratings = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Default"]

        records = []
        for i in range(1, n_borrowers + 1):
            ind = random.choice(industries)
            principal = round(float(np.random.lognormal(14.0, 1.0)), 2)
            interest_spread_bps = random.choice([175, 225, 300, 425, 600])
            dscr = round(float(np.random.normal(1.45, 0.35)), 2)
            pd_pct = round(max(0.01, min(25.0, (1.8 / max(0.5, dscr)) * 1.5)), 2)
            rating_idx = min(len(ratings) - 1, max(0, int(pd_pct // 2.5)))

            records.append({
                "facility_id": f"FAC-{i:05d}",
                "borrower_name": f"{ind} Holdings {i}",
                "industry_sector": ind,
                "committed_principal_usd": principal,
                "interest_spread_bps": interest_spread_bps,
                "debt_service_coverage_ratio": dscr,
                "probability_of_default_pct": pd_pct,
                "credit_risk_rating": ratings[rating_idx],
                "covenant_compliant": bool(dscr >= 1.20),
            })

        return pd.DataFrame(records)
