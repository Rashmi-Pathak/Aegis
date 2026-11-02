"""AEGIS Contextual & Multi-Armed Bandit Dynamic Mitigation Engine
Balances Exploration and Exploitation across competing mitigation policies using Upper Confidence Bound (UCB1).
"""
from typing import List, Dict, Any
import numpy as np

class MultiArmedBanditEngine:
    @staticmethod
    def select_action_ucb1(
        action_names: List[str],
        action_pulls: List[int],
        action_rewards: List[float],
        exploration_constant_c: float = 1.414,
    ) -> Dict[str, Any]:
        """Selects optimal mitigation action via UCB1 index: Q(a) + c * sqrt(ln(N) / N_a)."""
        total_pulls = sum(action_pulls)

        # If any arm has 0 pulls, explore it immediately
        for i, pulls in enumerate(action_pulls):
            if pulls == 0:
                return {
                    "selected_action": action_names[i],
                    "reason": "Pure Exploration (Untested Mitigation Lever)",
                    "ucb_scores": {action_names[k]: float("inf") if action_pulls[k] == 0 else 0.0 for k in range(len(action_names))},
                }

        ucb_values = []
        for i in range(len(action_names)):
            avg_reward = action_rewards[i] / action_pulls[i]
            exploration_bonus = exploration_constant_c * np.sqrt(np.log(total_pulls) / action_pulls[i])
            ucb_values.append(avg_reward + exploration_bonus)

        best_idx = int(np.argmax(ucb_values))

        return {
            "selected_action": action_names[best_idx],
            "highest_ucb_index": round(float(ucb_values[best_idx]), 3),
            "ucb_scores": {action_names[i]: round(float(ucb_values[i]), 3) for i in range(len(action_names))},
            "reason": "Exploitation / Uncertainty Bound Maximization",
        }
