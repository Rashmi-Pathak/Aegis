"""AEGIS Synthetic Clean Energy & Utility Grid Data Generator
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
