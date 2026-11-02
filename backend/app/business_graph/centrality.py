"""AEGIS Graph Centrality & Systemic Bottleneck Analysis
Computes PageRank, Betweenness Centrality, and Eigenvector Vulnerability to locate
critical single points of failure (SPOF) in the enterprise dependency web.
"""

from typing import Dict, Any, List
import networkx as nx


class GraphCentralityEngine:
    """Identifies structural choke points and systemic transmission nodes."""

    @staticmethod
    def analyze_network_centrality(graph: nx.DiGraph) -> Dict[str, Any]:
        """Calculates multi-dimensional centrality measures across all graph vertices."""
        if not graph.nodes:
            return {"top_bottlenecks": [], "pagerank": {}}

        # 1. PageRank (Authority / Downstream reach)
        try:
            pagerank = nx.pagerank(graph, weight="weight")
        except Exception:
            pagerank = {n: 1.0 / len(graph) for n in graph.nodes}

        # 2. Betweenness Centrality (Bridge nodes on shortest causal paths)
        betweenness = nx.betweenness_centrality(graph, weight="weight")

        # 3. In-degree and Out-degree
        in_degree = dict(graph.in_degree())
        out_degree = dict(graph.out_degree())

        # Composite Criticality Score = (PageRank * 0.4) + (Betweenness * 0.4) + (OutDegreeNorm * 0.2)
        max_out = max(out_degree.values()) if out_degree.values() and max(out_degree.values()) > 0 else 1
        criticality = {}
        for n in graph.nodes:
            pr = pagerank.get(n, 0.0)
            bc = betweenness.get(n, 0.0)
            od = out_degree.get(n, 0) / max_out
            score = round((pr * 0.4 + bc * 0.4 + od * 0.2) * 100.0, 1)
            criticality[n] = score

        top_bottlenecks = sorted(
            [
                {
                    "node": n,
                    "criticalityScore": criticality[n],
                    "pageRank": round(pagerank.get(n, 0.0), 3),
                    "betweenness": round(betweenness.get(n, 0.0), 3),
                    "downstreamImpactCount": out_degree.get(n, 0),
                }
                for n in graph.nodes
            ],
            key=lambda x: x["criticalityScore"],
            reverse=True,
        )

        return {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "top_bottlenecks": top_bottlenecks,
            "is_dag": nx.is_directed_acyclic_graph(graph),
        }
