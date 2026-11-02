import pytest
import numpy as np
from app.forecasting.metrics import ForecastMetrics
from app.forecasting.time_series import ClassicalForecaster
from app.forecasting.ml_forecaster import MLForecaster
from app.risk_engine.scoring import RiskScorer
from app.risk_engine.exposure import RiskExposureEngine
from app.risk_engine.monte_carlo import MonteCarloEngine
from app.business_graph.graph_builder import BusinessGraphBuilder
from app.business_graph.centrality import GraphCentralityEngine
from app.business_graph.causal_inference import CausalInferenceEngine
from app.decision_engine.optimization import DecisionOptimizer
from app.data_quality.drift import DataDriftDetector

def test_forecast_metrics():
    actuals = [100.0, 105.0, 110.0]
    preds = [102.0, 104.0, 108.0]
    errors = ForecastMetrics.evaluate_all(actuals, preds)
    assert errors["mae"] == 1.667
    assert errors["mape"] > 0

def test_exponential_smoothing():
    series = [100.0, 105.0, 110.0, 115.0, 120.0, 125.0]
    res = ClassicalForecaster.double_exponential_smoothing(series, horizon=4)
    assert len(res["forecast"]) == 4
    assert res["forecast"][-1] > res["forecast"][0]

def test_ml_forecaster():
    series = [float(x) for x in range(25)]
    res = MLForecaster.forecast(series, horizon=3)
    assert len(res["forecast"]) == 3
    assert "p10" in res and "p90" in res

def test_risk_scorer():
    res = RiskScorer.calculate_risk_score(probability=0.95, financial_impact_score=95.0)
    assert res["severity"] == "critical"
    assert res["risk_score"] >= 75.0

def test_var_cvar():
    returns = [-0.02, -0.01, 0.01, 0.02, -0.05, 0.03, -0.08]
    res = RiskExposureEngine.calculate_var_cvar(returns, portfolio_value=1000000.0)
    assert res["var_amount"] > 0
    assert res["cvar_expected_shortfall"] >= res["var_amount"]

def test_monte_carlo():
    res = MonteCarloEngine.simulate_revenue_ebitda(
        baseline_revenue=100.0,
        baseline_ebitda=15.0,
        n_iterations=500,
    )
    assert res["iterations_run"] == 500
    assert "expected_ebitda_p50" in res

def test_business_graph_and_centrality():
    twin = BusinessGraphBuilder.create_default_primelogix_digital_twin()
    graph_dict = twin.to_json_dict()
    assert len(graph_dict["nodes"]) >= 10
    assert len(graph_dict["edges"]) >= 10

    centrality = GraphCentralityEngine.analyze_network_centrality(twin.graph)
    assert len(centrality["top_bottlenecks"]) > 0

    paths = CausalInferenceEngine.find_all_causal_paths(twin.graph, "fuel_energy", "gross_margin")
    assert len(paths) > 0

def test_decision_optimizer():
    instruments = [
        {"name": "Diesel Forward Swap", "cost_per_unit": 5000, "risk_mitigated_per_unit": 12, "max_units": 10},
        {"name": "Spot Fleet Dynamic Routing", "cost_per_unit": 2000, "risk_mitigated_per_unit": 8, "max_units": 15},
    ]
    res = DecisionOptimizer.allocate_hedging_budget(total_budget=50000, hedging_instruments=instruments)
    assert res["allocated_expenditure"] <= 50000
    assert res["total_risk_points_reduced"] > 0

def test_data_drift():
    baseline = np.random.normal(50, 5, 200)
    shifted = np.random.normal(80, 5, 200)  # Heavy mean shift
    res = DataDriftDetector.calculate_psi(baseline, shifted)
    assert res["drift_detected"] is True
    assert res["psi"] > 0.25
