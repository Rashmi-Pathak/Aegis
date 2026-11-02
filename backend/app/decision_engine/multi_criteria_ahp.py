"""AEGIS Analytic Hierarchy Process (AHP) Decision Analysis
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
