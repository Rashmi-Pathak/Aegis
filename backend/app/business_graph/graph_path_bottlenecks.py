"""AEGIS Ford-Fulkerson Max-Flow / Min-Cut Supply Chain Bottleneck Engine
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
