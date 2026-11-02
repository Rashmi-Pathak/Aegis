"""AEGIS Deep Forecasting Test Suite
Verifies Croston intermittent demand, ARIMA AIC order selection, Quantile regression bounds,
and Cash Flow Runway forecasting models.
"""
import pytest
import numpy as np
from app.forecasting.cashflow_forecast import CashFlowForecaster
from app.forecasting.churn_forecast import ChurnForecaster
from app.forecasting.demand_forecast import DemandForecaster
from app.forecasting.inventory_forecast import InventoryForecaster
from app.forecasting.revenue_forecast import RevenueForecaster
from app.forecasting.risk_forecast import RiskEscalationForecaster
from app.forecasting.arima import AutoARIMAEvaluator
from app.forecasting.hierarchical import HierarchicalReconciler
from app.forecasting.quantile_regression import QuantileLossForecaster

def test_cashflow_forecaster():
    history = [150000.0, 180000.0, 120000.0, 210000.0, 190000.0]
    res = CashFlowForecaster.forecast_cash_flow(history, current_balance=500000.0, horizon_months=6)
    assert len(res["projected_monthly_balances"]) == 6
    assert res["is_runway_positive"] is True

def test_churn_forecaster():
    res = ChurnForecaster.forecast_churn_rate(active_customer_count=500, historical_churn_rates=[0.02, 0.025, 0.018], n_periods=4)
    assert len(res["projected_active_customers"]) == 4
    assert res["projected_active_customers"][-1] < 500

def test_croston_demand():
    intermittent = [0.0, 0.0, 45.0, 0.0, 0.0, 0.0, 52.0, 0.0, 48.0]
    res = DemandForecaster.croston_intermittent_forecast(intermittent, horizon=3)
    assert res["is_intermittent"] is True
    assert res["estimated_demand_per_period"] > 0

def test_inventory_depletion():
    demand = [10.0, 15.0, 20.0, 25.0, 30.0]
    replenish = [{"day": 3, "units": 50.0}]
    res = InventoryForecaster.forecast_stock_depletion(current_stock=40.0, forecasted_daily_demand=demand, replenishment_orders=replenish)
    assert len(res["projected_depletion"]) == 5
    assert res["stockout_projected"] is True
    assert res["stockout_day"] == 5

def test_arima_order_selection():
    np.random.seed(42)
    series = list(np.cumsum(np.random.normal(0, 1, 60)) + 100)
    res = AutoARIMAEvaluator.select_best_ar_order(series, max_p=3)
    assert res["best_p_order"] in [1, 2, 3]
    assert len(res["coefficients"]) == res["best_p_order"]

def test_hierarchical_reconciliation():
    bottom = {"SKU_A": [10.0, 12.0], "SKU_B": [20.0, 22.0]}
    res = HierarchicalReconciler.reconcile_bottom_up(bottom, {"SKU_A": 1.0, "SKU_B": 1.0})
    assert res["reconciled_total"] == [30.0, 34.0]

def test_quantile_loss():
    forecast = [100.0, 110.0, 120.0]
    residuals = [-5.0, -2.0, 0.0, 3.0, 7.0]
    intervals = QuantileLossForecaster.estimate_asymmetric_intervals(forecast, residuals)
    assert "P10" in intervals and "P90" in intervals
    assert intervals["P10"][0] < intervals["P90"][0]
