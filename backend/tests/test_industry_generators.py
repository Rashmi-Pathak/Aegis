"""AEGIS Multi-Industry Vertical Generator Test Suite
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
