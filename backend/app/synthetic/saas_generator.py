"""AEGIS Synthetic SaaS & B2B Subscription Data Generator
Generates MRR/ARR waterfalls, net expansion, seat expansions, contractions, and churn events.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class SaaSEnterpriseGenerator:
    PLANS = [
        ("Starter", 49.0, 5),
        ("Professional", 199.0, 20),
        ("Enterprise Core", 999.0, 100),
        ("Strategic Global", 4999.0, 500),
    ]

    @classmethod
    def generate_subscription_lifecycle(
        cls,
        n_accounts: int = 400,
        start_year: int = 2024,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        np.random.seed(seed)
        random.seed(seed)

        accounts = []
        billings = []

        for i in range(1, n_accounts + 1):
            plan_name, monthly_mrr, base_seats = random.choice(cls.PLANS)
            start_month = random.randint(1, 24)
            is_churned = bool(random.random() < 0.12)
            churn_month = random.randint(start_month + 3, 24) if is_churned else None

            acc_id = f"SUB-{i:05d}"
            accounts.append({
                "account_id": acc_id,
                "company_name": f"Cloud Tech Co {i}",
                "plan_tier": plan_name,
                "contract_mrr_usd": monthly_mrr,
                "allocated_seats": base_seats,
                "contract_start_month": start_month,
                "churn_month": churn_month,
                "is_active": not is_churned,
            })

            end_m = churn_month if is_churned and churn_month else 24
            for m in range(start_month, end_m + 1):
                expansion_factor = 1.0 + (0.05 * max(0, m - start_month))
                effective_mrr = monthly_mrr * expansion_factor
                billings.append({
                    "invoice_id": f"INV-{acc_id}-{m:02d}",
                    "account_id": acc_id,
                    "billing_month": m,
                    "billed_mrr": round(float(effective_mrr), 2),
                    "active_users": int(base_seats * expansion_factor),
                    "payment_status": "Paid" if random.random() > 0.02 else "Overdue",
                })

        return {
            "accounts": pd.DataFrame(accounts),
            "billings": pd.DataFrame(billings),
        }
