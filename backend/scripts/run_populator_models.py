import os

FILES = {
    "backend/app/synthetic/saas_generator.py": '''"""AEGIS Synthetic SaaS & B2B Subscription Data Generator
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
''',
    "backend/app/synthetic/retail_generator.py": '''"""AEGIS Synthetic Omni-Channel Retail Data Generator
Generates point-of-sale transactions, store foot-traffic, and inventory replenishment flows.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class RetailEnterpriseGenerator:
    CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Health & Beauty", "Automotive Goods"]

    @classmethod
    def generate_retail_ecosystem(
        cls,
        n_stores: int = 25,
        n_skus: int = 150,
        n_transactions: int = 2000,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        np.random.seed(seed)
        random.seed(seed)

        stores = []
        for s in range(1, n_stores + 1):
            stores.append({
                "store_id": f"STR-{s:03d}",
                "location": f"Metro Hub {s}",
                "sqft": random.choice([15000, 25000, 50000]),
                "daily_footfall_mean": random.randint(1200, 4500),
            })

        skus = []
        for k in range(1, n_skus + 1):
            cat = random.choice(cls.CATEGORIES)
            cost = round(float(np.random.uniform(5.0, 150.0)), 2)
            margin = random.uniform(0.25, 0.55)
            price = round(cost / (1.0 - margin), 2)
            skus.append({
                "sku_id": f"SKU-{k:04d}",
                "category": cat,
                "unit_cost": cost,
                "retail_price": price,
                "reorder_point": random.randint(20, 100),
            })

        txns = []
        store_ids = [s["store_id"] for s in stores]
        sku_lookup = {s["sku_id"]: s for s in skus}
        sku_ids = list(sku_lookup.keys())

        for t in range(1, n_transactions + 1):
            chosen_sku = sku_lookup[random.choice(sku_ids)]
            qty = random.randint(1, 4)
            rev = round(chosen_sku["retail_price"] * qty, 2)
            cogs = round(chosen_sku["unit_cost"] * qty, 2)

            txns.append({
                "transaction_id": f"TXN-{t:07d}",
                "store_id": random.choice(store_ids),
                "sku_id": chosen_sku["sku_id"],
                "quantity": qty,
                "revenue": rev,
                "cogs": cogs,
                "gross_margin": round(rev - cogs, 2),
                "channel": random.choice(["In-Store POS", "Online Pick-up (BOPIS)", "E-Commerce Ship-to-Home"]),
            })

        return {
            "stores": pd.DataFrame(stores),
            "skus": pd.DataFrame(skus),
            "transactions": pd.DataFrame(txns),
        }
''',
    "backend/app/synthetic/energy_generator.py": '''"""AEGIS Synthetic Clean Energy & Utility Grid Data Generator
Generates wind turbine and solar inverter telemetry, megawatt output, and grid frequency deviation.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class EnergyGridGenerator:
    @classmethod
    def generate_telemetry_stream(
        cls,
        n_turbines: int = 50,
        n_intervals: int = 288,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        rows = []
        for t in range(1, n_turbines + 1):
            base_capacity_mw = random.choice([2.5, 3.4, 4.2])
            wind_speeds = np.random.weibull(a=2.2, size=n_intervals) * 6.5

            for i in range(n_intervals):
                ws = wind_speeds[i]
                if ws < 3.0 or ws > 25.0:
                    power = 0.0
                else:
                    power = min(base_capacity_mw, base_capacity_mw * ((ws - 3.0) / 9.0) ** 3)

                gearbox_temp = 45.0 + (power * 8.5) + np.random.normal(0, 1.2)
                if t == 7 and i > 150:
                    gearbox_temp += 28.0

                rows.append({
                    "asset_id": f"WTG-{t:03d}",
                    "interval_step": i,
                    "wind_speed_ms": round(float(ws), 2),
                    "power_output_mw": round(float(power), 3),
                    "gearbox_temp_celsius": round(float(gearbox_temp), 1),
                    "grid_frequency_hz": round(float(np.random.normal(50.0, 0.04)), 3),
                    "status": "Fault" if (t == 7 and i > 150) else "Optimal",
                })

        return pd.DataFrame(rows)
''',
    "backend/app/synthetic/fintech_generator.py": '''"""AEGIS Synthetic Commercial Banking & FinTech Loan Portfolio Generator
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
''',
    "backend/tests/test_synthetic_verticals.py": '''"""AEGIS Multi-Vertical Synthetic Data Test Suite
Verifies generation of SaaS, Retail, Energy, and Credit Portfolio records.
"""
import pytest
from app.synthetic.saas_generator import SaaSEnterpriseGenerator
from app.synthetic.retail_generator import RetailEnterpriseGenerator
from app.synthetic.energy_generator import EnergyGridGenerator
from app.synthetic.fintech_generator import CommercialCreditGenerator

def test_saas_generation():
    res = SaaSEnterpriseGenerator.generate_subscription_lifecycle(n_accounts=50)
    assert not res["accounts"].empty
    assert not res["billings"].empty
    assert "contract_mrr_usd" in res["accounts"].columns

def test_retail_generation():
    res = RetailEnterpriseGenerator.generate_retail_ecosystem(n_stores=5, n_skus=20, n_transactions=100)
    assert not res["stores"].empty
    assert not res["skus"].empty
    assert not res["transactions"].empty

def test_energy_telemetry():
    df = EnergyGridGenerator.generate_telemetry_stream(n_turbines=5, n_intervals=20)
    assert not df.empty
    assert "power_output_mw" in df.columns
    assert "gearbox_temp_celsius" in df.columns

def test_fintech_credit():
    df = CommercialCreditGenerator.generate_loan_book(n_borrowers=40)
    assert not df.empty
    assert "debt_service_coverage_ratio" in df.columns
    assert "credit_risk_rating" in df.columns
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Synthetic verticals populated successfully.")
