"""AEGIS State-Space Kalman & ESG Sustainability Test Suite."""
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
