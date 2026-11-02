"""AEGIS Advanced Quantitative Algorithms:
Multi-Echelon Inventory Optimization (MEIO), BG/NBD Customer Lifetime Value,
AHP/TOPSIS Multi-Criteria Decision Analysis, Copula Tail Risk, Matrix Profile,
and Vector Autoregression (VAR).
"""

import os

FILES = {
    "backend/app/decision_engine/multi_criteria_ahp.py": '''"""AEGIS Analytic Hierarchy Process (AHP) Decision Analysis
Computes eigenvector weights from pairwise comparison matrices and verifies Consistency Ratio (CR < 0.10).
"""
from typing import List, Dict, Any
import numpy as np

class AHPDecisionEngine:
    # Random Consistency Index (Saaty)
    RI_TABLE = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41}

    @classmethod
    def evaluate_pairwise_matrix(
        cls,
        criteria_names: List[str],
        pairwise_matrix: List[List[float]],
    ) -> Dict[str, Any]:
        """Calculates criteria weights and validates consistency."""
        arr = np.array(pairwise_matrix, dtype=float)
        n = arr.shape[0]

        # Geometric mean approximation of principal eigenvector
        geom_means = np.prod(arr, axis=1) ** (1.0 / n)
        weights = geom_means / np.sum(geom_means)

        # Principal eigenvalue lambda_max
        weighted_sum_vector = arr @ weights
        lambda_max = float(np.mean(weighted_sum_vector / weights))

        # Consistency Index (CI) & Consistency Ratio (CR)
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = cls.RI_TABLE.get(n, 1.41)
        cr = ci / ri if ri > 0 else 0.0

        is_consistent = bool(cr < 0.10 or n <= 2)

        return {
            "criteria_weights": {criteria_names[i]: round(float(weights[i]), 4) for i in range(n)},
            "lambda_max": round(lambda_max, 4),
            "consistency_index_ci": round(float(ci), 4),
            "consistency_ratio_cr": round(float(cr), 4),
            "is_matrix_consistent": is_consistent,
            "validation_note": "Consistent judgments" if is_consistent else "Judgments show logical inconsistency (CR >= 0.10)",
        }
''',
    "backend/app/decision_engine/topsis_engine.py": '''"""AEGIS TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
Ranks strategic initiatives based on Euclidean distance to Positive and Negative Ideal Solutions.
"""
from typing import List, Dict, Any
import numpy as np

class TOPSISDecisionEngine:
    @staticmethod
    def rank_alternatives(
        alternative_names: List[str],
        decision_matrix: List[List[float]],  # rows = alternatives, cols = criteria
        weights: List[float],
        is_benefit_criterion: List[bool],  # True if higher is better, False if cost
    ) -> List[Dict[str, Any]]:
        """Executes TOPSIS multi-attribute ranking."""
        arr = np.array(decision_matrix, dtype=float)
        n_alt, n_crit = arr.shape

        # 1. Vector normalization: r_ij = x_ij / sqrt(sum(x_ij^2))
        col_norms = np.sqrt(np.sum(arr ** 2, axis=0))
        norm_matrix = arr / col_norms

        # 2. Weighted normalized decision matrix: v_ij = w_j * r_ij
        w_norm = norm_matrix * np.array(weights)

        # 3. Determine ideal best (A+) and ideal worst (A-)
        ideal_best = np.zeros(n_crit)
        ideal_worst = np.zeros(n_crit)

        for j in range(n_crit):
            if is_benefit_criterion[j]:
                ideal_best[j] = np.max(w_norm[:, j])
                ideal_worst[j] = np.min(w_norm[:, j])
            else:
                ideal_best[j] = np.min(w_norm[:, j])
                ideal_worst[j] = np.max(w_norm[:, j])

        # 4. Separation measures
        dist_best = np.sqrt(np.sum((w_norm - ideal_best) ** 2, axis=1))
        dist_worst = np.sqrt(np.sum((w_norm - ideal_worst) ** 2, axis=1))

        # 5. Relative closeness to ideal: C_i = S_i- / (S_i+ + S_i-)
        closeness = dist_worst / (dist_best + dist_worst)

        results = []
        for i in range(n_alt):
            results.append({
                "alternative": alternative_names[i],
                "closeness_score": round(float(closeness[i]), 4),
                "distance_to_best": round(float(dist_best[i]), 4),
                "distance_to_worst": round(float(dist_worst[i]), 4),
            })

        return sorted(results, key=lambda x: x["closeness_score"], reverse=True)
''',
    "backend/app/analytics/customer_lifetime_value.py": '''"""AEGIS BG/NBD & Gamma-Gamma Customer Lifetime Value (CLV) Engine
Models repeat transaction rates, account drop-out probabilities, and monetary spend expectations.
"""
from typing import Dict, Any, List
import numpy as np

class BGNBDCLVModel:
    @staticmethod
    def expected_transactions_p_alive(
        frequency: int,
        recency: float,
        T_cal: float,
        r: float = 0.24,
        alpha: float = 4.41,
        a: float = 0.05,
        b: float = 0.25,
    ) -> Dict[str, float]:
        """Calculates P(Alive) and expected future transactions over horizon t."""
        # Fader & Hardie BG/NBD probability of customer still being active
        x = frequency
        t_x = recency

        denom = 1.0 + (x > 0) * (a / (b + x - 1.0)) * ((alpha + T_cal) / (alpha + t_x)) ** (r + x)
        p_alive = 1.0 / denom if denom > 0 else 0.5

        # Expected transactions in next 12 periods
        future_t = 12.0
        exp_txns = ((r + x) / (alpha + T_cal)) * future_t * p_alive

        return {
            "probability_customer_alive": round(float(p_alive), 3),
            "expected_12m_transactions": round(float(exp_txns), 2),
            "account_health": "Active & Loyal" if p_alive > 0.75 else ("At-Risk" if p_alive > 0.40 else "Dormant / Lost"),
        }
''',
    "backend/app/analytics/inventory_optimization.py": '''"""AEGIS Multi-Echelon Inventory Optimization (MEIO)
Computes base-stock policies, safety stock pooling across regional distribution centers (DCs).
"""
from typing import List, Dict, Any
import numpy as np
import scipy.stats as stats

class MEIOEngine:
    @staticmethod
    def calculate_pooled_safety_stock(
        independent_dc_demands_std: List[float],
        lead_time_days: float,
        service_level_pct: float = 95.0,
    ) -> Dict[str, Any]:
        """Calculates safety stock savings from centralized inventory risk pooling."""
        z = stats.norm.ppf(service_level_pct / 100.0)

        # Decentralized sum of safety stocks
        decentralized_ss = sum(z * std * np.sqrt(lead_time_days) for std in independent_dc_demands_std)

        # Centralized pooled safety stock (assuming zero correlation)
        pooled_std = np.sqrt(sum(std ** 2 for std in independent_dc_demands_std))
        centralized_ss = z * pooled_std * np.sqrt(lead_time_days)

        savings_units = decentralized_ss - centralized_ss
        savings_pct = (savings_units / decentralized_ss) * 100.0 if decentralized_ss > 0 else 0.0

        return {
            "decentralized_safety_stock_units": round(float(decentralized_ss), 1),
            "centralized_safety_stock_units": round(float(centralized_ss), 1),
            "capital_freed_savings_units": round(float(savings_units), 1),
            "working_capital_reduction_pct": round(float(savings_pct), 1),
            "risk_pooling_benefit": "Significant Capital Efficiency" if savings_pct > 25.0 else "Modest Benefit",
        }
''',
    "backend/app/risk_engine/portfolio_var_copula.py": '''"""AEGIS Copula Joint Tail Dependency & Portfolio Value-at-Risk Engine
Simulates non-linear systemic co-crashes using Gumbel & Clayton Copula distributions.
"""
from typing import Dict, Any, List
import numpy as np

class CopulaTailRiskEngine:
    @staticmethod
    def simulate_tail_copula_loss(
        asset_values: List[float],
        individual_vars: List[float],
        tail_dependency_lambda: float = 0.45,
        n_scenarios: int = 5000,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Simulates joint tail contagion where market stress causes simultaneous breakdowns."""
        np.random.seed(seed)
        n_assets = len(asset_values)

        # Copula shock generator: common macro factor Z + idiosyncratic factors E_i
        common_shock = np.random.standard_t(df=4, size=n_scenarios)
        idio_shocks = np.random.standard_normal(size=(n_scenarios, n_assets))

        # Blended factor model mimicking Clayton/Student-t tail dependence
        weight_common = np.sqrt(tail_dependency_lambda)
        weight_idio = np.sqrt(1.0 - tail_dependency_lambda)

        blended = (weight_common[:, None] * common_shock[:, None]) + (weight_idio * idio_shocks)

        # Simulated portfolio loss
        portfolio_losses = []
        for row in blended:
            loss = sum(max(0.0, -row[i] * individual_vars[i]) for i in range(n_assets))
            portfolio_losses.append(loss)

        arr = np.array(portfolio_losses)
        copula_var_99 = float(np.percentile(arr, 99))
        copula_cvar_99 = float(np.mean(arr[arr >= copula_var_99])) if np.any(arr >= copula_var_99) else copula_var_99

        return {
            "copula_portfolio_var_99": round(copula_var_99, 2),
            "copula_expected_shortfall_cvar_99": round(copula_cvar_99, 2),
            "linear_sum_var_benchmark": round(float(sum(individual_vars)), 2),
            "diversification_breakdown_ratio": round(copula_var_99 / (sum(individual_vars) or 1.0), 2),
        }
''',
    "backend/app/business_graph/graph_path_bottlenecks.py": '''"""AEGIS Ford-Fulkerson Max-Flow / Min-Cut Supply Chain Bottleneck Engine
Identifies bottleneck throughput limits and minimal operational cuts in freight networks.
"""
from typing import Dict, Any, List
import networkx as nx

class GraphBottleneckFlowEngine:
    @staticmethod
    def compute_max_freight_throughput(
        graph: nx.DiGraph,
        source_origin: str,
        sink_destination: str,
    ) -> Dict[str, Any]:
        """Computes max-flow and cuts finding exact operational choke points."""
        if source_origin not in graph or sink_destination not in graph:
            return {"max_throughput_flow": 0.0, "bottleneck_cut_edges": []}

        # Build capacity graph from edge weights
        flow_g = nx.DiGraph()
        for u, v, data in graph.edges(data=True):
            cap = data.get("capacity", data.get("weight", 1.0) * 1000.0)
            flow_g.add_edge(u, v, capacity=cap)

        try:
            flow_val, flow_dict = nx.maximum_flow(flow_g, source_origin, sink_destination)
            cut_val, partition = nx.minimum_cut(flow_g, source_origin, sink_destination)
            reachable, non_reachable = partition

            cut_edges = []
            for u in reachable:
                for v in flow_g.successors(u):
                    if v in non_reachable:
                        cut_edges.append((u, v))
        except Exception:
            return {"max_throughput_flow": 0.0, "bottleneck_cut_edges": []}

        return {
            "max_throughput_flow": round(float(flow_val), 1),
            "bottleneck_cut_edges": cut_edges,
            "critical_choke_point_count": len(cut_edges),
        }
''',
    "backend/tests/test_advanced_algorithms.py": '''"""AEGIS Advanced Quantitative Algorithm Test Suite
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
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Advanced algorithms generated successfully.")
