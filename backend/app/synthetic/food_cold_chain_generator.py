"""AEGIS Agriculture & Perishable Food Processing Generator
Generates harvest lot yields, cold storage temperature telemetry, and shelf-life decay curves.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class FoodColdChainGenerator:
    COMMODITIES = ["Organic Strawberries", "Dairy Creamery", "Frozen Poultry", "Fresh Atlantic Salmon"]

    @classmethod
    def generate_cold_chain_logs(
        cls,
        n_shipments: int = 300,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        records = []
        for i in range(1, n_shipments + 1):
            item = random.choice(cls.COMMODITIES)
            target_temp = 2.0 if "Frozen" not in item else -18.0
            actual_temp = target_temp + float(np.random.normal(0.0, 1.2))
            hours_in_transit = random.randint(12, 96)
            breach = bool(actual_temp > (target_temp + 3.0))

            spoilage_cost = round(random.randint(5000, 35000) * 0.40, 2) if breach else 0.0

            records.append({
                "consignment_id": f"FD-{i:05d}",
                "commodity": item,
                "target_temp_celsius": target_temp,
                "mean_actual_temp_celsius": round(actual_temp, 1),
                "transit_hours": hours_in_transit,
                "temperature_excursion_breach": breach,
                "spoilage_loss_usd": spoilage_cost,
            })

        return pd.DataFrame(records)
