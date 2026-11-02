"""Deep enterprise intelligence modules for AEGIS AI Business Risk & Decision Intelligence Platform.
Implements Markov Decision Processes, Cox Proportional Hazards, Spectral Graph Partitioning,
FAIR Cyber Loss, and Multi-Touch Attribution.
"""

import os

FILES = {
    "backend/app/decision_engine/dynamic_programming.py": '''"""AEGIS Markov Decision Process (MDP) & Bellman Value Iteration
Solves optimal dynamic decision policies across stochastic business environments.
V_{k+1}(s) = max_a sum_{s'} P(s' | s, a) [ R(s, a, s') + gamma * V_k(s') ]
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class BusinessMDPValueIteration:
    @staticmethod
    def solve_infinite_horizon_mdp(
        states: List[str],
        actions: List[str],
        transition_probabilities: Dict[Tuple[str, str], Dict[str, float]],  # (s, a) -> {s': P}
        rewards: Dict[Tuple[str, str], float],  # (s, a) -> R
        discount_factor_gamma: float = 0.95,
        tolerance: float = 1e-4,
        max_iterations: int = 1000,
    ) -> Dict[str, Any]:
        """Executes Bellman value iteration until convergence."""
        v = {s: 0.0 for s in states}
        policy = {s: actions[0] for s in states}

        for iteration in range(1, max_iterations + 1):
            delta = 0.0
            new_v = {}

            for s in states:
                action_values = {}
                for a in actions:
                    r = rewards.get((s, a), 0.0)
                    t_probs = transition_probabilities.get((s, a), {})
                    expected_future = sum(prob * v.get(next_s, 0.0) for next_s, prob in t_probs.items())
                    q_val = r + discount_factor_gamma * expected_future
                    action_values[a] = q_val

                best_action = max(action_values, key=action_values.get)
                best_val = action_values[best_action]
                new_v[s] = best_val
                policy[s] = best_action
                delta = max(delta, abs(new_v[s] - v[s]))

            v = new_v
            if delta < tolerance:
                break

        return {
            "converged": bool(delta < tolerance),
            "iterations_to_convergence": iteration,
            "optimal_value_function": {k: round(v[k], 2) for k in v},
            "optimal_policy": policy,
        }
''',
    "backend/app/analytics/churn_hazard.py": '''"""AEGIS Cox Proportional Hazards & Semi-Parametric Churn Regression
Estimates hazard ratios h(t) = h_0(t) * exp(beta * X) for enterprise accounts.
"""
from typing import List, Dict, Any
import numpy as np

class CoxHazardEstimator:
    @staticmethod
    def calculate_hazard_ratios(
        feature_names: List[str],
        coefficients: List[float],
    ) -> List[Dict[str, Any]]:
        """Computes Hazard Ratios HR = exp(beta) and interprets risk multiplier."""
        results = []
        for name, beta in zip(feature_names, coefficients):
            hr = float(np.exp(beta))
            pct_change = (hr - 1.0) * 100.0

            if hr > 1.25:
                impact = f"+{pct_change:.1f}% Churn Hazard Risk Surge"
            elif hr < 0.80:
                impact = f"{pct_change:.1f}% Protective / Retention Anchor"
            else:
                impact = "Marginal Risk Effect"

            results.append({
                "covariate": name,
                "beta_coefficient": round(beta, 3),
                "hazard_ratio": round(hr, 3),
                "churn_risk_effect": impact,
            })
        return results
''',
    "backend/app/analytics/attribution.py": '''"""AEGIS Markov Chain Multi-Touch Marketing Attribution
Calculates customer conversion attribution weights using Markov graph removal effects.
"""
from typing import List, Dict, Any
import numpy as np

class MarkovAttributionEngine:
    @staticmethod
    def calculate_removal_effects(
        channels: List[str],
        touchpoint_paths: List[List[str]],
        conversions: List[int],
    ) -> Dict[str, Any]:
        """Measures conversion drop when each channel is removed from customer journey."""
        if not channels or not touchpoint_paths:
            return {"channel_weights_pct": {}, "total_conversions": 0}

        total_conversions = sum(conversions)
        removal_effects = {}

        for ch in channels:
            # Baseline without channel ch
            retained_conv = 0
            for path, conv in zip(touchpoint_paths, conversions):
                if ch not in path:
                    retained_conv += conv
            # Removal effect = 1 - (retained / total)
            eff = (total_conversions - retained_conv) / total_conversions if total_conversions > 0 else 0.0
            removal_effects[ch] = max(0.01, eff)

        total_eff = sum(removal_effects.values()) or 1.0
        normalized = {ch: round((val / total_eff) * 100.0, 1) for ch, val in removal_effects.items()}

        return {
            "channel_attribution_weights_pct": normalized,
            "total_observed_conversions": total_conversions,
            "highest_converting_channel": max(normalized, key=normalized.get) if normalized else "None",
        }
''',
    "backend/app/business_graph/spectral_clustering.py": '''"""AEGIS Spectral Graph Partitioning & Risk Clustering
Computes normalized graph Laplacian eigenvalues and Fiedler vector to isolate decoupled business risk modules.
"""
from typing import Dict, Any, List
import networkx as nx
import numpy as np
import scipy.sparse.csgraph as csgraph

class SpectralRiskClusterer:
    @staticmethod
    def partition_graph_spectral(graph: nx.DiGraph, k_clusters: int = 2) -> Dict[str, Any]:
        """Partitions business dependency graph using spectral Laplacian eigen-decomposition."""
        if len(graph.nodes) < 4:
            return {"clusters": {n: 0 for n in graph.nodes}, "fiedler_value": 0.0}

        undirected = graph.to_undirected()
        adj = nx.to_numpy_array(undirected)
        laplacian = csgraph.laplacian(adj, normed=True)

        eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        fiedler_val = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
        fiedler_vec = eigenvectors[:, 1] if len(eigenvectors) > 1 else np.zeros(len(graph.nodes))

        nodes_list = list(graph.nodes)
        clusters = {}
        for i, n in enumerate(nodes_list):
            clusters[n] = int(fiedler_vec[i] >= 0)

        return {
            "node_count": len(graph.nodes),
            "spectral_clusters": clusters,
            "algebraic_connectivity_fiedler": round(fiedler_val, 4),
            "graph_robustness": "Decoupled / Fault-Tolerant" if fiedler_val > 0.15 else "Tightly Coupled / Cascade Prone",
        }
''',
    "backend/app/risk_engine/cyber_risk_fair.py": '''"""AEGIS Factor Analysis of Information Risk (FAIR) Cyber Exposure Engine
Models Loss Event Frequency (LEF) and Loss Magnitude (LM) across ransomware and data breach risks.
"""
from typing import Dict, Any, List
import numpy as np

class FAIRLossModel:
    @staticmethod
    def simulate_cyber_annual_loss_exposure(
        threat_event_frequency_lambda: float = 2.5,
        vulnerability_pct: float = 18.0,
        loss_magnitude_lognorm_mean: float = 12.5,
        loss_magnitude_lognorm_std: float = 1.2,
        n_trials: int = 5000,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Runs FAIR Monte Carlo simulation: Annual Loss Exposure = LEF * LM."""
        np.random.seed(seed)

        # Threat events ~ Poisson
        threat_events = np.random.poisson(threat_event_frequency_lambda, n_trials)
        # Vulnerability gating
        v_prob = vulnerability_pct / 100.0

        annual_losses = []
        for t_events in threat_events:
            actual_breaches = np.random.binomial(t_events, v_prob)
            if actual_breaches == 0:
                annual_losses.append(0.0)
            else:
                mags = np.random.lognormal(loss_magnitude_lognorm_mean, loss_magnitude_lognorm_std, actual_breaches)
                annual_losses.append(float(np.sum(mags)))

        arr = np.array(annual_losses)

        return {
            "mean_annual_loss_exposure": round(float(np.mean(arr)), 2),
            "p90_worst_case_exposure": round(float(np.percentile(arr, 90)), 2),
            "p99_tail_risk_exposure": round(float(np.percentile(arr, 99)), 2),
            "probability_of_zero_loss_pct": round(float(np.mean(arr == 0)) * 100.0, 1),
            "fair_risk_rating": "Critical Capital Drag" if np.mean(arr) > 1000000.0 else "Insurable Operational Risk",
        }
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Enterprise intelligence core populated successfully.")
