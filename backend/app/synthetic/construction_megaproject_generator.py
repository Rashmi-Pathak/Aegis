"""AEGIS EPC Infrastructure & Construction Megaproject Data Generator
Generates Critical Path Method (CPM) milestones, concrete pouring telemetry, and change order variances.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class ConstructionEPCGenerator:
    MILESTONES = [
        ("Substructure Foundations", 180, 25000000.0),
        ("Structural Steel Superstructure", 240, 45000000.0),
        ("HVAC & MEP Systems Rough-In", 150, 18000000.0),
        ("Curtain Wall Glazing", 120, 15000000.0),
        ("Interior Architectural Fit-Out", 160, 22000000.0),
        ("Commissioning & Life Safety", 90, 8000000.0),
    ]

    @classmethod
    def generate_project_schedule(
        cls,
        project_name: str = "Metropolitan Transit Tunnel & Station Package",
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        rows = []
        for name, planned_days, budget in cls.MILESTONES:
            slip_days = int(np.random.gamma(shape=1.8, scale=12.0) - 8.0)
            actual_days = planned_days + max(0, slip_days)
            cost_overrun = float(np.random.beta(2, 20) * budget) if slip_days > 0 else 0.0

            rows.append({
                "milestone": name,
                "planned_duration_days": planned_days,
                "actual_projected_days": actual_days,
                "schedule_slip_days": max(0, slip_days),
                "budget_usd": round(budget, 2),
                "cost_overrun_usd": round(cost_overrun, 2),
                "liquidated_damages_risk": bool(slip_days > 25),
            })

        return pd.DataFrame(rows)
