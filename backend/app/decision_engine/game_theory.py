"""AEGIS Strategic Game Theory & Minimax Regret Matrix Solver
Solves competitive bidding games, supplier negotiation games, and Minimax Regret choices.
"""

from typing import List, Dict, Any
import numpy as np


class GameTheoryEngine:
    """Minimax regret decision criteria under deep Knightian uncertainty (unknown probabilities)."""

    @staticmethod
    def minimax_regret_analysis(
        payoff_matrix: List[List[float]],  # rows = actions, cols = states of the world
        action_names: List[str],
        state_names: List[str],
    ) -> Dict[str, Any]:
        """Calculates the Regret (Opportunity Loss) matrix and selects action minimizing maximum regret.
        Regret_ij = max_k(Payoff_kj) - Payoff_ij
        """
        arr = np.array(payoff_matrix, dtype=float)
        n_actions, n_states = arr.shape

        # Column-wise maximum payoffs
        best_in_states = np.max(arr, axis=0)

        # Regret matrix
        regret = best_in_states - arr

        # Maximum regret per action
        max_regrets = np.max(regret, axis=1)

        best_action_idx = int(np.argmin(max_regrets))

        actions_report = []
        for i in range(n_actions):
            actions_report.append({
                "action": action_names[i] if i < len(action_names) else f"Action {i}",
                "max_regret": round(float(max_regrets[i]), 2),
                "regret_vector": [round(float(r), 2) for r in regret[i]],
            })

        return {
            "recommended_action": action_names[best_action_idx] if best_action_idx < len(action_names) else f"Action {best_action_idx}",
            "minimax_regret_value": round(float(max_regrets[best_action_idx]), 2),
            "state_benchmarks": [round(float(b), 2) for b in best_in_states],
            "action_evaluations": actions_report,
        }
