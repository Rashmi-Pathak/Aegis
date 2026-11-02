"""AEGIS Decision Tree Evaluation & Expected Monetary Value (EMV) Roll-Back Engine
Solves multi-stage decision problems under uncertainty using backwards induction.
"""

from typing import List, Dict, Any, Optional


class DecisionTreeEvaluator:
    """Evaluates decision branches, chance events, and terminal payoffs to select optimal policies."""

    @staticmethod
    def evaluate_chance_node(branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates Expected Monetary Value (EMV) of a chance node:
        EMV = Sum(Probability_i * Payoff_i)
        """
        emv = 0.0
        prob_sum = 0.0
        for b in branches:
            p = b.get("probability", 0.0)
            payoff = b.get("payoff", 0.0)
            prob_sum += p
            emv += p * payoff

        return {
            "expected_monetary_value": round(emv, 2),
            "normalized_probability_sum": round(prob_sum, 2),
            "branch_count": len(branches),
        }

    @classmethod
    def rollback_decision_tree(cls, tree: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively rolls back decision and chance nodes to discover optimal path."""
        node_type = tree.get("type", "terminal")

        if node_type == "terminal":
            return {
                "id": tree.get("id"),
                "optimal_value": round(float(tree.get("payoff", 0.0)), 2),
                "chosen_action": None,
            }

        elif node_type == "chance":
            emv = 0.0
            children_eval = []
            for branch in tree.get("branches", []):
                child_res = cls.rollback_decision_tree(branch["node"])
                p = branch.get("probability", 1.0)
                emv += p * child_res["optimal_value"]
                children_eval.append({**branch, "result": child_res})

            return {
                "id": tree.get("id"),
                "optimal_value": round(emv, 2),
                "type": "chance",
                "branches": children_eval,
            }

        elif node_type == "decision":
            # Maximize EMV across alternatives
            best_val = -float("inf")
            best_action = None
            alternatives_eval = []

            for option in tree.get("options", []):
                cost = option.get("cost", 0.0)
                child_res = cls.rollback_decision_tree(option["node"])
                net_val = child_res["optimal_value"] - cost
                alternatives_eval.append({
                    "action": option.get("action"),
                    "cost": cost,
                    "net_value": round(net_val, 2),
                    "sub_tree": child_res,
                })
                if net_val > best_val:
                    best_val = net_val
                    best_action = option.get("action")

            return {
                "id": tree.get("id"),
                "optimal_value": round(best_val, 2),
                "chosen_action": best_action,
                "type": "decision",
                "evaluated_options": alternatives_eval,
            }

        return {"optimal_value": 0.0}
