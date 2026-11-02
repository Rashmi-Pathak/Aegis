"""AEGIS Cellular & Fiber Infrastructure Telemetry Generator
Generates cell tower traffic, drop-call rates, fiber packet latency, and subscriber bandwidth churn.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class TelecomEnterpriseGenerator:
    @classmethod
    def generate_network_telemetry(
        cls,
        n_towers: int = 80,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        towers = []
        for t in range(1, n_towers + 1):
            bandwidth_gbps = float(np.random.uniform(10.0, 100.0))
            drop_call_pct = float(np.random.beta(1.5, 95.0) * 100.0)
            latency_ms = float(np.random.normal(18.0, 3.5))

            towers.append({
                "tower_id": f"TWR-{t:04d}",
                "metro_region": random.choice(["North", "South", "East", "West", "Central"]),
                "peak_bandwidth_gbps": round(bandwidth_gbps, 1),
                "drop_call_rate_pct": round(drop_call_pct, 2),
                "latency_milliseconds": round(latency_ms, 1),
                "power_backup_hours": round(float(np.random.uniform(4.0, 18.0)), 1),
                "service_degradation_alert": bool(drop_call_pct > 3.0 or latency_ms > 30.0),
            })

        return pd.DataFrame(towers)
