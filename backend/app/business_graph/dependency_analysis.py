"""AEGIS Graph Dependency Analysis & Upstream/Downstream Tracing
Analyzes upstream supply dependencies and downstream customer revenue blast radius.
"""
from typing import Dict, Any, List
import networkx as nx

class GraphDependencyAnalyzer:
    @staticmethod
    def get_blast_radius(graph: nx.DiGraph, root_node: str) -> Dict[str, Any]:
        """Calculates all downstream nodes reachable from root node."""
        if root_node not in graph:
            return {"impacted_nodes": [], "blast_radius_score": 0.0}

        downstream = list(nx.descendants(graph, root_node))
        upstream = list(nx.ancestors(graph, root_node))
        total_nodes = len(graph.nodes)
        blast_score = (len(downstream) / total_nodes) * 100.0 if total_nodes > 0 else 0.0

        return {
            "root_node": root_node,
            "downstream_impacted_nodes": downstream,
            "upstream_dependency_nodes": upstream,
            "downstream_count": len(downstream),
            "blast_radius_percentage": round(blast_score, 1),
        }
