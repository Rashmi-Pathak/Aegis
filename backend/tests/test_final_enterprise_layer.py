"""AEGIS Final Enterprise Layer Test Suite
Verifies 50 Financial Ratios, Climate Physical Risk, Geopolitical Tariffs,
and Vector Autoregression (VAR).
"""
import pytest
from app.analytics.financial_ratios import EnterpriseRatioSuite
from app.risk_engine.climate_physical_risk import PhysicalClimateRiskEngine
from app.risk_engine.geopolitical_risk import GeopoliticalRiskEngine
from app.forecasting.var_forecaster import VectorAutoregressionForecaster

def test_financial_ratios_suite():
    res = EnterpriseRatioSuite.compute_all_ratios(
        revenue=100000000.0,
        cogs=60000000.0,
        operating_expenses=20000000.0,
        ebit=20000000.0,
        ebitda=25000000.0,
        interest_expense=2500000.0,
        tax_expense=3500000.0,
        net_income=14000000.0,
        cash_and_equivalents=15000000.0,
        marketable_securities=5000000.0,
        accounts_receivable=12000000.0,
        inventory=8000000.0,
        total_current_assets=40000000.0,
        property_plant_equipment=60000000.0,
        total_assets=100000000.0,
        accounts_payable=10000000.0,
        short_term_debt=5000000.0,
        total_current_liabilities=20000000.0,
        long_term_debt=20000000.0,
        total_liabilities=45000000.0,
        shareholders_equity=55000000.0,
        operating_cash_flow=22000000.0,
        capital_expenditures=8000000.0,
    )
    assert res["liquidity"]["current_ratio"] == 2.0
    assert res["profitability"]["gross_margin_pct"] == 40.0
    assert res["leverage_solvency"]["interest_coverage_ratio"] == 8.0
    assert res["cash_flow_quality"]["free_cash_flow_usd"] == 14000000.0

def test_climate_physical_risk():
    res = PhysicalClimateRiskEngine.evaluate_facility_exposure(
        facility_name="Rotterdam Gateway Terminal",
        replacement_asset_value_usd=80000000.0,
        is_coastal_hub=True,
        elevation_meters=2.4,
        regional_heat_index_days=18,
    )
    assert res["expected_annual_climate_loss_usd"] > 0
    assert res["climate_value_at_risk_99_usd"] > res["expected_annual_climate_loss_usd"]

def test_geopolitical_risk():
    res = GeopoliticalRiskEngine.evaluate_freight_rerouting_shock(
        choke_point_key="suez_canal",
        annual_teu_volume=5000.0,
        active_blockade_status=True,
        tariff_escalation_pct=10.0,
        cargo_value_usd=20000000.0,
    )
    assert res["annual_rerouting_cost_usd"] == 4250000.0
    assert res["total_geopolitical_financial_drag"] > 4250000.0

def test_var_multivariate():
    # 3 co-integrated series over 15 periods
    data = [[100 + i * 2, 50 + i * 1.5, 30 + i * 0.8] for i in range(15)]
    res = VectorAutoregressionForecaster.forecast_multivariate_system(
        variables=["FreightVolume", "DieselPrice", "DriverCost"],
        data_matrix=data,
        horizon_steps=3,
    )
    assert len(res["forecasts_by_variable"]["FreightVolume"]) == 3
