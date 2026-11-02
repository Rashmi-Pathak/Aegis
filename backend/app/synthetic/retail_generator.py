"""AEGIS Synthetic Omni-Channel Retail Data Generator
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
