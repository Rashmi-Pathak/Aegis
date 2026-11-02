"""AEGIS Deep Decision Intelligence Test Suite
Verifies Decision Tree EMV Roll-back, Simplex Resource Allocation, Minimax Regret,
and Pareto Frontier initiatives.
"""
import pytest
from app.decision_engine.decision_trees import DecisionTreeEvaluator
from app.decision_engine.linear_programming import ResourceOptimizer
from app.decision_engine.game_theory import GameTheoryEngine
from app.decision_engine.tradeoff_analyzer import TradeoffAnalyzer
from app.decision_engine.approval_rules import ApprovalWorkflowEngine
from app.decision_engine.impact_estimator import DecisionImpactEstimator

def test_decision_tree_rollback():
    tree = {
        "id": "root",
        "type": "decision",
        "options": [
            {
                "action": "Hedge Diesel",
                "cost": 10000.0,
                "node": {"type": "terminal", "payoff": 80000.0, "id": "t1"},
            },
            {
                "action": "Spot Market Only",
                "cost": 0.0,
                "node": {"type": "terminal", "payoff": 40000.0, "id": "t2"},
            },
        ],
    }
    res = DecisionTreeEvaluator.rollback_decision_tree(tree)
    assert res["chosen_action"] == "Hedge Diesel"
    assert res["optimal_value"] == 70000.0

def test_linear_fleet_allocation():
    res = ResourceOptimizer.solve_fleet_route_allocation(
        costs_per_route=[120.0, 150.0],
        min_demand_deliveries=[10.0, 10.0],
        max_driver_capacities=[50.0, 50.0],
        max_total_budget=50000.0,
    )
    assert res["success"] is True
    assert res["optimal_cost"] == 2700.0

def test_minimax_regret():
    payoffs = [
        [100.0, 50.0],
        [70.0, 90.0],
    ]
    res = GameTheoryEngine.minimax_regret_analysis(payoffs, ["Option A", "Option B"], ["State 1", "State 2"])
    assert "recommended_action" in res

def test_pareto_tradeoff():
    initiatives = [
        {"name": "Fast Cheap", "cost": 1000, "risk_reduction": 20, "weeks": 2},
        {"name": "Slow Expensive", "cost": 5000, "risk_reduction": 10, "weeks": 10},
    ]
    res = TradeoffAnalyzer.identify_pareto_optimal_initiatives(initiatives)
    assert res[0]["is_pareto_optimal"] is True

def test_approval_hierarchy():
    res = ApprovalWorkflowEngine.determine_approval_hierarchy(1500000.0, risk_score=85.0)
    assert "Board of Directors" in res["approval_tier"]

def test_impact_estimator():
    res = DecisionImpactEstimator.estimate_initiative_impact(
        baseline_revenue=1000000.0,
        baseline_cost=800000.0,
        cost_reduction_pct=5.0,
        revenue_uplift_pct=2.0,
        implementation_cost=20000.0,
    )
    assert res["is_value_accretive"] is True
    assert res["margin_expansion_bps"] > 0
