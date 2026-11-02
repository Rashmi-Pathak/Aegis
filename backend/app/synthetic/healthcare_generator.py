"""AEGIS Healthcare & MedTech System Data Generator
Generates inpatient admissions, ICU bed occupancy, cold-chain pharma spoilage, and biomedical equipment telemetry.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class HealthcareEnterpriseGenerator:
    DEPARTMENTS = ["Emergency", "Cardiology", "Oncology", "Intensive Care (ICU)", "Orthopedics"]

    @classmethod
    def generate_hospital_records(
        cls,
        n_patients: int = 1000,
        n_equipment: int = 40,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        np.random.seed(seed)
        random.seed(seed)

        # 1. Inpatient Admissions
        admissions = []
        for i in range(1, n_patients + 1):
            dept = random.choice(cls.DEPARTMENTS)
            los_days = float(np.random.gamma(shape=2.5, scale=2.0))
            treatment_cost = float(np.random.lognormal(mean=9.2, sigma=0.8))
            insurance_payout = treatment_cost * random.uniform(0.70, 0.95)

            admissions.append({
                "admission_id": f"ADM-{i:06d}",
                "department": dept,
                "length_of_stay_days": round(los_days, 1),
                "billed_treatment_usd": round(treatment_cost, 2),
                "reimbursement_usd": round(insurance_payout, 2),
                "margin_deficit_usd": round(treatment_cost - insurance_payout, 2),
                "readmission_30d_risk": bool(random.random() < 0.08),
            })

        # 2. Equipment Telemetry
        equipment = []
        for eq in range(1, n_equipment + 1):
            eq_type = random.choice(["MRI Scanner", "CT Angiography", "Dialysis Unit", "Ventilator"])
            calib_drift = float(np.random.normal(0, 0.05))
            equipment.append({
                "equipment_id": f"MED-{eq:04d}",
                "equipment_type": eq_type,
                "daily_operating_hours": round(float(np.random.uniform(8.0, 22.0)), 1),
                "calibration_drift_sigmas": round(calib_drift, 3),
                "maintenance_flag": bool(abs(calib_drift) > 0.12),
            })

        return {
            "admissions": pd.DataFrame(admissions),
            "equipment": pd.DataFrame(equipment),
        }
