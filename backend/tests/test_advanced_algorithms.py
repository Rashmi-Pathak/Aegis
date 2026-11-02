"""AEGIS Advanced Quantitative Algorithm Test Suite
Verifies AHP Consistency, TOPSIS Ranking, MEIO Inventory Pooling,
BG/NBD CLV estimation, Copula tail risk, and Max-Flow Min-Cut bottlenecks.
"""
import pytest
import networkx as nx
from app.decision_engine.multi_criteria_ahp import AHPDecisionEngine
from app.decision_engine.topsis_engine import TOPSISDecisionEngine
from app.analytics.customer_lifetime_value import BGNBDCLVModel
from app.analytics.inventory_optimization import MEIOEngine
from app.risk_engine.portfolio_var_copula import CopulaTailRiskEngine
from app.business_graph.graph_path_bottlenecks import GraphBottleneckFlowEngine

def test_ahp_consistent():
    matrix = [
        [1.0, 3.0, 5.0],
        [1/3, 1.0, 2.0],
        [1/5, 1/2, 1.0],
    ]
    res = AHPDecisionEngine.evaluate_pairwise_matrix(["Cost", "Quality", "Speed"], matrix)
    assert res["is_matrix_consistent"] is True
    assert res["consistency_ratio_cr"] < 0.10

def test_topsis_ranking():
    matrix = [
        [250.0, 16.0, 12.0],
        [200.0, 20.0, 8.0],
        [300.0, 28.0, 16.0],
    ]
    weights = [0.4, 0.3, 0.3]
    benefits = [False, True, True]  # Cost is negative criterion
    res = TOPSISDecisionEngine.rank_alternatives(["Vendor A", "Vendor B", "Vendor C"], matrix, weights, benefits)
    assert len(res) == 3
    assert res[0]["closeness_score"] >= res[1]["closeness_score"]

def test_bgnbd_clv():
    res = BGNBDCLVModel.expected_transactions_p_alive(frequency=5, recency=12.0, T_cal=15.0)
    assert res["probability_customer_alive"] > 0.5
    assert res["expected_12m_transactions"] > 0

def test_meio_inventory_pooling():
    stds = [15.0, 18.0, 12.0, 14.0]
    res = MEIOEngine.calculate_pooled_safety_stock(stds, lead_time_days=4.0)
    assert res["capital_freed_savings_units"] > 0
    assert res["working_capital_reduction_pct"] > 20.0

def test_copula_tail_risk():
    res = CopulaTailRiskEngine.simulate_tail_copula_loss(
        asset_values=[1000000.0, 1500000.0],
        individual_vars=[50000.0, 80000.0],
        tail_dependency_lambda=0.4,
    )
    assert res["copula_portfolio_var_99"] > 0

def test_max_flow_bottleneck():
    g = nx.DiGraph()
    g.add_edge("factory", "port", capacity=100.0)
    g.add_edge("port", "warehouse", capacity=60.0)
    g.add_edge("warehouse", "customer", capacity=80.0)
    res = GraphBottleneckFlowEngine.compute_max_freight_throughput(g, "factory", "customer")
    assert res["max_throughput_flow"] == 60.0
    assert len(res["bottleneck_cut_edges"]) > 0
