import pytest
from app.analytics.kpis import KPICalculator
from app.analytics.revenue import RevenueAnalytics
from app.analytics.finance import FinancialAnalytics
from app.analytics.customers import CustomerAnalytics
from app.analytics.inventory import InventoryAnalytics
from app.analytics.operations import OperationsAnalytics

def test_kpi_growth_rate():
    assert KPICalculator.calculate_growth_rate(120.0, 100.0) == 20.0
    assert KPICalculator.calculate_growth_rate(80.0, 100.0) == -20.0
    assert KPICalculator.calculate_growth_rate(100.0, 0.0) == 0.0

def test_gross_and_operating_margins():
    assert KPICalculator.gross_margin_percentage(100.0, 60.0) == 40.0
    assert KPICalculator.operating_margin_percentage(15.0, 100.0) == 15.0

def test_altman_z_score():
    res = KPICalculator.altman_z_score(
        working_capital=20.0,
        retained_earnings=30.0,
        ebit=15.0,
        market_equity=80.0,
        sales=100.0,
        total_assets=100.0,
        total_liabilities=50.0,
    )
    assert "z_score" in res
    assert res["zone"] == "Safe Zone"
    assert res["probability_of_distress"] < 0.10

def test_arr_waterfall():
    res = RevenueAnalytics.calculate_arr_waterfall(
        starting_arr=100.0,
        new_bookings=25.0,
        expansion_arr=10.0,
        contraction_arr=3.0,
        churned_arr=2.0,
    )
    assert res["ending_arr"] == 130.0
    assert res["net_revenue_retention_pct"] == 105.0

def test_inventory_eoq():
    eoq = InventoryAnalytics.calculate_eoq(
        annual_demand=10000,
        ordering_cost_fixed=50,
        annual_holding_cost_per_unit=4,
    )
    assert eoq["economic_order_quantity"] == 500.0
    assert eoq["optimal_orders_per_year"] == 20.0

def test_operations_otif():
    otif = OperationsAnalytics.calculate_otif(
        total_shipments=100,
        on_time_shipments=95,
        in_full_shipments=96,
        damage_free_shipments=98,
    )
    assert otif["otif_compliance_pct"] == 95.0
    assert otif["sla_status"] == "Optimal"
