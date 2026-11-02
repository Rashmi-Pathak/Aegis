"""AEGIS Graph Risk Propagation & Contagion Modeling
Models systemic contagion and cascading shocks across enterprise business dependencies.
"""

from typing import Dict, Any, List, Set
import numpy as np


class RiskPropagationEngine:
    """Propagates localized operational disruptions across downstream nodes using Markov cascades."""

    @staticmethod
    def simulate_cascade(
        adjacency_dict: Dict[str, List[Dict[str, Any]]],
        initial_shocked_nodes: Dict[str, float],  # node_id -> shock_magnitude (0 to 100)
        damping_factor: float = 0.75,
        max_depth: int = 5,
    ) -> Dict[str, Any]:
        """Calculates downstream blast radius and final stress levels across network."""
        current_stress = dict(initial_shocked_nodes)
        visited_nodes: Set[str] = set(initial_shocked_nodes.keys())
        propagation_log = []

        frontier = list(initial_shocked_nodes.items())

        depth = 0
        while frontier and depth < max_depth:
            next_frontier = []
            depth += 1

            for source_node, shock in frontier:
                edges = adjacency_dict.get(source_node, [])
                for edge in edges:
                    target = edge["target"]
                    weight = edge.get("weight", 0.5)

                    induced_stress = shock * weight * (damping_factor ** depth)

                    if induced_stress > 5.0:  # Significance threshold
                        old_stress = current_stress.get(target, 0.0)
                        new_stress = min(100.0, old_stress + induced_stress)
                        current_stress[target] = new_stress

                        propagation_log.append({
                            "depth": depth,
                            "source": source_node,
                            "target": target,
                            "transmitted_shock": round(induced_stress, 1),
                            "target_accumulated_stress": round(new_stress, 1),
                        })

                        if target not in visited_nodes:
                            visited_nodes.add(target)
                            next_frontier.append((target, induced_stress))

            frontier = next_frontier

        # Highlight most vulnerable downstream nodes
        vulnerable_nodes = sorted(
            [{"node": k, "stress_level": round(v, 1)} for k, v in current_stress.items()],
            key=lambda x: x["stress_level"],
            reverse=True,
        )

        return {
            "initial_shocks": initial_shocked_nodes,
            "total_impacted_nodes": len(current_stress),
            "max_cascade_depth": depth,
            "final_stress_levels": {k: round(v, 1) for k, v in current_stress.items()},
            "most_vulnerable_nodes": vulnerable_nodes,
            "propagation_trail": propagation_log,
        }
