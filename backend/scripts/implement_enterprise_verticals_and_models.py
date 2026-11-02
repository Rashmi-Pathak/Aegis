"""AEGIS Enterprise Vertical Generators & Deep Analytical Engines:
Healthcare, Aerospace, Automotive, Manufacturing, Telecom, Construction EPC,
State-Space Kalman Filtering, ESG Sustainability, and ABC Costing.
"""

import os

FILES = {
    "backend/app/synthetic/healthcare_generator.py": '''"""AEGIS Healthcare & MedTech System Data Generator
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
''',
    "backend/app/synthetic/aerospace_generator.py": '''"""AEGIS Aerospace & Defense Fleet Reliability Generator
Generates jet engine cycle hours, vibration harmonics, turnaround times, and FAA regulatory compliance.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class AerospaceEnterpriseGenerator:
    @classmethod
    def generate_fleet_telemetry(
        cls,
        n_aircraft: int = 35,
        n_flights: int = 800,
        seed: int = 42,
    ) -> Dict[str, pd.DataFrame]:
        np.random.seed(seed)
        random.seed(seed)

        aircraft = []
        for a in range(1, n_aircraft + 1):
            aircraft.append({
                "tail_number": f"N{a:03d}AG",
                "aircraft_model": random.choice(["Boeing 777F", "Airbus A330-200F", "Boeing 747-8F"]),
                "flight_hours_total": random.randint(4500, 28000),
                "engine_cycles_since_overhaul": random.randint(200, 3500),
                "scheduled_maintenance_due_hours": random.randint(150, 1200),
            })

        flights = []
        tail_ids = [ac["tail_number"] for ac in aircraft]
        for f in range(1, n_flights + 1):
            dist_nm = random.randint(800, 5200)
            fuel_burn_lbs = dist_nm * random.uniform(18.5, 24.0)
            vibration = float(np.random.weibull(1.8) * 0.45)

            flights.append({
                "flight_id": f"FLT-{f:06d}",
                "tail_number": random.choice(tail_ids),
                "distance_nautical_miles": dist_nm,
                "fuel_burn_lbs": round(fuel_burn_lbs, 1),
                "engine_vibration_index": round(vibration, 3),
                "delay_minutes": max(0, int(np.random.exponential(15.0) - 10.0)),
                "structural_anomaly": bool(vibration > 1.2),
            })

        return {
            "aircraft": pd.DataFrame(aircraft),
            "flights": pd.DataFrame(flights),
        }
''',
    "backend/app/synthetic/manufacturing_generator.py": '''"""AEGIS Manufacturing & CNC Precision Assembly Generator
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
''',
    "backend/app/synthetic/telecom_generator.py": '''"""AEGIS Cellular & Fiber Infrastructure Telemetry Generator
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
''',
    "backend/app/analytics/cost_allocation_engine.py": '''"""AEGIS Activity-Based Costing (ABC) & Cost Center Variance Engine
Allocates corporate overhead to product lines, sales channels, and geographic business units.
"""
from typing import Dict, Any, List
import numpy as np

class ActivityBasedCostingEngine:
    @staticmethod
    def allocate_overhead(
        total_overhead_pool_usd: float,
        cost_drivers: List[Dict[str, Any]],  # activity, driver_name, units_consumed, cost_per_driver_unit
    ) -> Dict[str, Any]:
        """Allocates corporate overhead pools based on consumption rates."""
        allocated_activities = []
        total_allocated = 0.0

        for d in cost_drivers:
            activity = d.get("activity", "General Overhead")
            units = d.get("units_consumed", 0.0)
            rate = d.get("cost_per_driver_unit", 1.0)
            cost = units * rate
            total_allocated += cost
            allocated_activities.append({
                "activity": activity,
                "driver": d.get("driver_name", "Units"),
                "allocated_amount_usd": round(cost, 2),
            })

        unallocated = max(0.0, total_overhead_pool_usd - total_allocated)

        return {
            "total_overhead_pool_usd": round(total_overhead_pool_usd, 2),
            "total_allocated_usd": round(total_allocated, 2),
            "unallocated_variance_usd": round(unallocated, 2),
            "allocated_breakdown": allocated_activities,
            "absorption_rate_pct": round((total_allocated / total_overhead_pool_usd) * 100.0, 1) if total_overhead_pool_usd > 0 else 100.0,
        }
''',
    "backend/app/forecasting/state_space_models.py": '''"""AEGIS State-Space Local Linear Trend & Kalman Filtering
Separates true underlying business trajectory from high-frequency observation noise.
x_{t} = F * x_{t-1} + w_t
y_{t} = H * x_{t} + v_t
"""
from typing import List, Dict, Any, Tuple
import numpy as np

class KalmanFilterForecaster:
    @staticmethod
    def filter_and_forecast(
        observations: List[float],
        process_variance_q: float = 0.5,
        observation_variance_r: float = 2.0,
        horizon_steps: int = 5,
    ) -> Dict[str, Any]:
        """Executes 1D Kalman filter and projects forward trajectory."""
        if not observations:
            return {"filtered_states": [], "forecast": []}

        # Initial state estimates: [level, trend]
        x = np.array([observations[0], 0.0])
        P = np.eye(2) * 5.0

        F = np.array([[1.0, 1.0], [0.0, 1.0]])  # State transition matrix
        H = np.array([[1.0, 0.0]])             # Measurement matrix
        Q = np.eye(2) * process_variance_q
        R = np.array([[observation_variance_r]])

        filtered_levels = []

        for z in observations:
            # 1. Predict step
            x_pred = F @ x
            P_pred = F @ P @ F.T + Q

            # 2. Update step
            y_innov = z - (H @ x_pred)
            S = H @ P_pred @ H.T + R
            K = P_pred @ H.T @ np.linalg.inv(S)

            x = x_pred + K @ y_innov
            P = (np.eye(2) - K @ H) @ P_pred

            filtered_levels.append(round(float(x[0]), 2))

        # 3. Forecast future steps
        forecast = []
        curr_x = x.copy()
        for _ in range(horizon_steps):
            curr_x = F @ curr_x
            forecast.append(round(float(curr_x[0]), 2))

        return {
            "filtered_historical_levels": filtered_levels,
            "final_estimated_level": round(float(x[0]), 2),
            "final_estimated_trend": round(float(x[1]), 3),
            "forecast": forecast,
        }
''',
    "backend/app/risk_engine/esg_sustainability_risk.py": '''"""AEGIS Corporate ESG & Carbon Emission Liability Risk Engine
Calculates carbon border tax liabilities (CBAM), Scope 1/2/3 penalties, and ESG discount factors.
"""
from typing import Dict, Any, List

class ESGSustainabilityRiskEngine:
    @staticmethod
    def calculate_carbon_liability(
        annual_scope_1_metric_tons: float,
        annual_scope_2_metric_tons: float,
        annual_scope_3_metric_tons: float,
        projected_carbon_price_per_ton_usd: float = 85.0,
        eu_cbam_export_percentage: float = 25.0,
    ) -> Dict[str, Any]:
        """Calculates projected carbon emission regulatory liability."""
        total_emissions = (
            annual_scope_1_metric_tons
            + annual_scope_2_metric_tons
            + (annual_scope_3_metric_tons * 0.40)  # Standard regulatory attribution
        )

        gross_liability = total_emissions * projected_carbon_price_per_ton_usd
        cbam_tariff = gross_liability * (eu_cbam_export_percentage / 100.0)

        return {
            "total_accountable_emissions_mt": round(total_emissions, 1),
            "projected_carbon_price_usd": projected_carbon_price_per_ton_usd,
            "annual_carbon_tax_liability_usd": round(gross_liability, 2),
            "eu_cbam_tariff_drag_usd": round(cbam_tariff, 2),
            "esg_climate_transition_risk": "Severe Regulatory Drag" if gross_liability > 5000000.0 else "Managed Carbon Posture",
        }
''',
    "backend/tests/test_industry_generators.py": '''"""AEGIS Multi-Industry Vertical Generator Test Suite
Verifies Healthcare, Aerospace, Manufacturing, and Telecom generators.
"""
import pytest
from app.synthetic.healthcare_generator import HealthcareEnterpriseGenerator
from app.synthetic.aerospace_generator import AerospaceEnterpriseGenerator
from app.synthetic.manufacturing_generator import ManufacturingEnterpriseGenerator
from app.synthetic.telecom_generator import TelecomEnterpriseGenerator

def test_healthcare_generator():
    res = HealthcareEnterpriseGenerator.generate_hospital_records(n_patients=50, n_equipment=10)
    assert not res["admissions"].empty
    assert not res["equipment"].empty
    assert "billed_treatment_usd" in res["admissions"].columns

def test_aerospace_generator():
    res = AerospaceEnterpriseGenerator.generate_fleet_telemetry(n_aircraft=5, n_flights=25)
    assert not res["aircraft"].empty
    assert not res["flights"].empty
    assert "fuel_burn_lbs" in res["flights"].columns

def test_manufacturing_generator():
    res = ManufacturingEnterpriseGenerator.generate_factory_telemetry(n_machines=5, n_work_orders=30)
    assert not res["workorders" if "workorders" in res else "work_orders"].empty

def test_telecom_generator():
    df = TelecomEnterpriseGenerator.generate_network_telemetry(n_towers=15)
    assert not df.empty
    assert "peak_bandwidth_gbps" in df.columns
''',
    "backend/tests/test_kalman_and_esg.py": '''"""AEGIS State-Space Kalman & ESG Sustainability Test Suite."""
import pytest
from app.forecasting.state_space_models import KalmanFilterForecaster
from app.risk_engine.esg_sustainability_risk import ESGSustainabilityRiskEngine
from app.analytics.cost_allocation_engine import ActivityBasedCostingEngine

def test_kalman_filter():
    obs = [100.0, 102.0, 104.0, 107.0, 109.0, 112.0]
    res = KalmanFilterForecaster.filter_and_forecast(obs, horizon_steps=3)
    assert len(res["filtered_historical_levels"]) == 6
    assert len(res["forecast"]) == 3
    assert res["final_estimated_trend"] > 0

def test_esg_carbon_risk():
    res = ESGSustainabilityRiskEngine.calculate_carbon_liability(
        annual_scope_1_metric_tons=50000.0,
        annual_scope_2_metric_tons=30000.0,
        annual_scope_3_metric_tons=100000.0,
        projected_carbon_price_per_ton_usd=90.0,
    )
    assert res["annual_carbon_tax_liability_usd"] > 0
    assert "total_accountable_emissions_mt" in res

def test_abc_cost_allocation():
    drivers = [
        {"activity": "Quality Inspection", "units_consumed": 200, "cost_per_driver_unit": 50.0},
        {"activity": "Machine Setup", "units_consumed": 40, "cost_per_driver_unit": 250.0},
    ]
    res = ActivityBasedCostingEngine.allocate_overhead(30000.0, drivers)
    assert res["total_allocated_usd"] == 20000.0
    assert res["unallocated_variance_usd"] == 10000.0
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Enterprise verticals and models populated successfully.")
