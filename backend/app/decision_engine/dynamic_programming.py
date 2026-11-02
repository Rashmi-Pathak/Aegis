"""AEGIS Markov Decision Process (MDP) & Bellman Value Iteration
Solves optimal dynamic decision policies across stochastic business environments.
V_{k+1}(s) = max_a sum_{s'} P(s' | s, a) [ R(s, a, s') + gamma * V_k(s') ]
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class BusinessMDPValueIteration:
    @staticmethod
    def solve_infinite_horizon_mdp(
        states: List[str],
        actions: List[str],
        transition_probabilities: Dict[Tuple[str, str], Dict[str, float]],  # (s, a) -> {s': P}
        rewards: Dict[Tuple[str, str], float],  # (s, a) -> R
        discount_factor_gamma: float = 0.95,
        tolerance: float = 1e-4,
        max_iterations: int = 1000,
    ) -> Dict[str, Any]:
        """Executes Bellman value iteration until convergence."""
        v = {s: 0.0 for s in states}
        policy = {s: actions[0] for s in states}

        for iteration in range(1, max_iterations + 1):
            delta = 0.0
            new_v = {}

            for s in states:
                action_values = {}
                for a in actions:
                    r = rewards.get((s, a), 0.0)
                    t_probs = transition_probabilities.get((s, a), {})
                    expected_future = sum(prob * v.get(next_s, 0.0) for next_s, prob in t_probs.items())
                    q_val = r + discount_factor_gamma * expected_future
                    action_values[a] = q_val

                best_action = max(action_values, key=action_values.get)
                best_val = action_values[best_action]
                new_v[s] = best_val
                policy[s] = best_action
                delta = max(delta, abs(new_v[s] - v[s]))

            v = new_v
            if delta < tolerance:
                break

        return {
            "converged": bool(delta < tolerance),
            "iterations_to_convergence": iteration,
            "optimal_value_function": {k: round(v[k], 2) for k in v},
            "optimal_policy": policy,
        }
