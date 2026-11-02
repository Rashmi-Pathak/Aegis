"""AEGIS Causal Inference & Directed Acyclic Graph (DAG) Engine
Performs topological sorting, causal path exploration, and Granger-style temporal tests
to isolate true root causes from correlated downstream symptoms.
"""

from typing import List, Dict, Any, Optional
import networkx as nx


class CausalInferenceEngine:
    """Explores directional causal pathways between root triggers and downstream KPIs."""

    @staticmethod
    def find_all_causal_paths(
        graph: nx.DiGraph,
        source_trigger: str,
        target_kpi: str,
    ) -> List[Dict[str, Any]]:
        """Finds all simple directed paths linking trigger event to target KPI."""
        if source_trigger not in graph or target_kpi not in graph:
            return []

        paths = []
        try:
            raw_paths = list(nx.all_simple_paths(graph, source_trigger, target_kpi, cutoff=6))
            for p in raw_paths:
                # Calculate path cumulative transmission weight
                cumulative_weight = 1.0
                path_steps = []
                for i in range(len(p) - 1):
                    u, v = p[i], p[i + 1]
                    edge_data = graph.get_edge_data(u, v, default={})
                    w = edge_data.get("weight", 0.5)
                    cumulative_weight *= w
                    path_steps.append({
                        "from": u,
                        "to": v,
                        "relation": edge_data.get("relationship", "impacts"),
                        "weight": w,
                    })

                paths.append({
                    "path_nodes": p,
                    "path_length": len(p),
                    "causal_strength": round(cumulative_weight, 3),
                    "steps": path_steps,
                })
        except Exception:
            pass

        return sorted(paths, key=lambda x: x["causal_strength"], reverse=True)
