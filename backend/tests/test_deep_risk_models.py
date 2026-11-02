"""AEGIS Deep Quantitative Risk Test Suite
Verifies Merton Distance-to-Default, Basel III Liquidity Coverage Ratio (LCR),
Bayesian Belief Updating, and Graph Cascade Contagion models.
"""
import pytest
from app.risk_engine.bayesian_network import BayesianRiskUpdater
from app.risk_engine.credit_risk import CreditRiskEngine
from app.risk_engine.liquidity_stress import LiquidityStressEngine
from app.risk_engine.propagation import RiskPropagationEngine
from app.risk_engine.severity import SeverityClassifier

def test_bayesian_updater():
    res = BayesianRiskUpdater.update_posterior_probability(
        prior_probability=0.10,
        evidence_likelihood_given_risk=0.90,
        evidence_likelihood_given_normal=0.05,
    )
    assert res["posterior_probability"] > 0.60
    assert res["bayes_factor"] == 18.0

def test_merton_default():
    res = CreditRiskEngine.merton_distance_to_default(
        asset_value=150000000.0,
        debt_face_value=100000000.0,
        asset_volatility=0.25,
    )
    assert res["distance_to_default_sigmas"] > 1.0
    assert res["structural_probability_of_default_pct"] < 25.0

def test_liquidity_stress():
    res = LiquidityStressEngine.simulate_30_day_liquidity_stress(
        cash_and_equivalents=25000000.0,
        committed_undrawn_credit_lines=15000000.0,
        contractual_debt_maturities_30d=5000000.0,
        operational_payables_30d=15000000.0,
        contingent_fuel_price_spike_outflow=3000000.0,
    )
    assert res["liquidity_coverage_ratio_pct"] > 100.0
    assert res["liquidity_cushion_status"] == "Strong Liquidity Surplus"

def test_risk_propagation_cascade():
    adj = {
        "fuel": [{"target": "trucking", "weight": 0.8}],
        "trucking": [{"target": "retail", "weight": 0.9}],
    }
    shocks = {"fuel": 80.0}
    res = RiskPropagationEngine.simulate_cascade(adj, shocks)
    assert "trucking" in res["final_stress_levels"]
    assert "retail" in res["final_stress_levels"]

def test_severity_classifier():
    assert SeverityClassifier.get_tier(85.0) == "critical"
    assert SeverityClassifier.get_tier(60.0) == "high"
    assert SeverityClassifier.get_tier(35.0) == "medium"
    assert SeverityClassifier.get_tier(10.0) == "low"
