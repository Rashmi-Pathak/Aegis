"""AEGIS TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
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
