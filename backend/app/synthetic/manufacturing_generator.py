"""AEGIS Manufacturing & CNC Precision Assembly Generator
Generates work orders, spindle vibration, cutting tool wear, and scrap defect rates.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class ManufacturingEnterpriseGenerator:
    @classmethod
    def generate_factory_telemetry(
        cls,
        n_machines: int = 24,
        n_work_orders: int = 600,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        np.random.seed(seed)
        random.seed(seed)

        work_orders = []
        for w in range(1, n_work_orders + 1):
            batch_size = random.randint(50, 500)
            defect_rate = float(np.random.beta(a=2, b=45))
            defects = int(round(batch_size * defect_rate))
            cycle_time_mins = float(np.random.normal(45.0, 5.0))

            work_orders.append({
                "order_id": f"WO-{w:06d}",
                "part_type": random.choice(["Titanium Turbine Blade", "Landing Gear Actuator", "Hydraulic Manifold"]),
                "batch_size_units": batch_size,
                "defective_units": defects,
                "scrap_cost_usd": round(defects * 450.0, 2),
                "cycle_time_minutes": round(cycle_time_mins, 1),
                "machine_id": f"CNC-{random.randint(1, n_machines):02d}",
            })

        return {"work_orders": pd.DataFrame(work_orders)}
