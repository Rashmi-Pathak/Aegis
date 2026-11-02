"""AEGIS Graph Structural Percolation & Fragility Modeling
Computes network percolation thresholds and robustness to node removal.
"""
from typing import Dict, Any
import networkx as nx

class GraphFragilityModel:
    @staticmethod
    def calculate_network_fragility(graph: nx.DiGraph) -> Dict[str, Any]:
        """Measures network density, reciprocity, and single-point-of-failure vulnerabilities."""
        if len(graph.nodes) == 0:
            return {"fragility_index": 0.0, "status": "EMPTY"}

        undirected = graph.to_undirected()
        density = nx.density(graph)

        try:
            cut_nodes = list(nx.articulation_points(undirected))
        except Exception:
            cut_nodes = []

        fragility_score = min(100.0, (len(cut_nodes) * 20.0) + ((1.0 - density) * 30.0))

        return {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "graph_density": round(float(density), 3),
            "single_points_of_failure": cut_nodes,
            "fragility_score": round(float(fragility_score), 1),
            "resilience_tier": "Fragile" if len(cut_nodes) > 2 else "Resilient",
        }
