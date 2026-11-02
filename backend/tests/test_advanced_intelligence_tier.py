"""AEGIS Advanced Intelligence Tier Test Suite."""
import pytest
from app.analytics.earned_value_management import EVMAnalysisEngine
from app.analytics.credit_transition_matrix import CreditTransitionMatrixEngine
from app.forecasting.theta_method_forecaster import ThetaForecaster
from app.decision_engine.multi_armed_bandit import MultiArmedBanditEngine
from app.decision_engine.real_options_valuation import RealOptionsBinomialLattice
from app.risk_engine.regulatory_basel_iv_rwa import BaselIVCapitalEngine
from app.risk_engine.black_swan_extreme_value import ExtremeValueTheoryEngine

def test_evm_metrics():
    res = EVMAnalysisEngine.compute_evm_metrics(
        planned_value_pv=1000000.0,
        earned_value_ev=900000.0,
        actual_cost_ac=950000.0,
        budget_at_completion_bac=5000000.0,
    )
    assert res["cost_performance_index_cpi"] < 1.0
    assert res["schedule_performance_index_spi"] < 1.0
    assert res["estimate_at_completion_eac"] > 5000000.0

def test_credit_transition():
    res = CreditTransitionMatrixEngine.project_n_year_default_probability("BBB", n_years=3)
    assert res["cumulative_default_probability_pct"] > 0
    assert "Default" in res["projected_rating_probabilities"]

def test_theta_forecaster():
    series = [100.0, 102.0, 105.0, 108.0, 112.0]
    res = ThetaForecaster.forecast_theta(series, horizon=3)
    assert len(res["forecast"]) == 3
    assert res["linear_slope"] > 0

def test_bandit_ucb1():
    names = ["Action A", "Action B"]
    pulls = [10, 10]
    rewards = [25.0, 80.0]  # Action B has much higher reward
    res = MultiArmedBanditEngine.select_action_ucb1(names, pulls, rewards)
    assert res["selected_action"] == "Action B"

def test_real_options_crr():
    res = RealOptionsBinomialLattice.price_expansion_option(
        underlying_asset_value_S=10000000.0,
        expansion_capital_cost_K=8000000.0,
    )
    assert res["real_option_value"] > 0
    assert res["expanded_strategic_npv"] > 2000000.0

def test_basel_iv_rwa():
    exposures = [
        {"exposure_amount": 10000000.0, "rating": "AAA"},
        {"exposure_amount": 20000000.0, "rating": "BBB"},
    ]
    res = BaselIVCapitalEngine.calculate_capital_requirement(exposures)
    assert res["total_risk_weighted_assets_usd"] > 0
    assert res["minimum_tier1_capital_required_usd"] > 0

def test_extreme_value_theory():
    losses = list(range(10, 100)) + [250.0, 480.0, 950.0]
    res = ExtremeValueTheoryEngine.peaks_over_threshold_gpd(losses)
    assert res["black_swan_loss_p999_usd"] > 100.0
