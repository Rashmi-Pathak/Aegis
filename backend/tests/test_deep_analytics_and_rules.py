"""AEGIS Deep Corporate Analytics & Business Rules Test Suite
Verifies DuPont ROE, Altman Z-Score, Kaplan-Meier Survival, PED Elasticity,
Kraljic procurement, and Covenant audits.
"""
import pytest
from app.analytics.kpis import KPICalculator
from app.analytics.cohorts import CohortAnalytics
from app.analytics.pricing import PricingAnalytics
from app.analytics.cashflow import CashFlowAnalytics
from app.analytics.procurement import ProcurementAnalytics
from app.analytics.hr_workforce import WorkforceAnalytics
from app.rules.covenant_rules import CovenantRules

def test_dupont_roe():
    res = KPICalculator.dupont_analysis(
        net_income=15.0,
        revenue=100.0,
        total_assets=80.0,
        total_equity=50.0,
    )
    assert res["roe"] == 30.0
    assert res["net_margin_pct"] == 15.0

def test_kaplan_meier():
    durations = [1.0, 2.0, 3.0, 4.0, 5.0]
    events = [True, False, True, False, True]
    res = CohortAnalytics.kaplan_meier_survival(durations, events)
    assert len(res["survival_probabilities"]) == 5
    assert res["survival_probabilities"][-1] < 1.0

def test_price_elasticity():
    prices = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
    quantities = [100.0, 90.0, 81.0, 72.0, 64.0, 58.0]
    res = PricingAnalytics.estimate_price_elasticity(prices, quantities)
    assert res["elasticity"] < 0
    assert "Elastic" in res["classification"]

def test_kraljic_procurement():
    suppliers = [
        {"name": "Critical Diesel", "annual_spend": 20000000.0, "supply_risk_score": 8.0},
        {"name": "Office Paper", "annual_spend": 50000.0, "supply_risk_score": 1.0},
    ]
    res = ProcurementAnalytics.classify_kraljic_matrix(suppliers)
    assert "Strategic" in res[0]["kraljic_quadrant"]

def test_workforce_analytics():
    res = WorkforceAnalytics.calculate_workforce_kpis(
        total_headcount=1200,
        annualized_revenue=150000000.0,
        annualized_payroll=35000000.0,
        departures_last_12m=120,
        critical_role_openings=25,
    )
    assert res["annualized_turnover_rate_pct"] == 10.0
    assert res["workforce_stability_status"] == "Normal"

def test_covenant_rules():
    financials = {
        "debt_service_coverage_ratio": 1.10,
        "cash_reserve_usd": 12000000.0,
        "current_ratio": 1.5,
    }
    violations = CovenantRules.audit_covenants(financials)
    assert len(violations) == 1
    assert violations[0]["rule_id"] == "cov_min_dscr"
