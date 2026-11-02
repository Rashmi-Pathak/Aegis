"""AEGIS Multi-Vertical Synthetic Data Test Suite
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
