"""AEGIS Spectral Graph Partitioning & Risk Clustering
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
