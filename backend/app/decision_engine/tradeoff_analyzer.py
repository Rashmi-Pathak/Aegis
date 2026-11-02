"""AEGIS Multi-Objective Trade-Off & Pareto Frontier Analysis
Plots initiatives along Capital Required vs Risk Reduction vs Time to Value.
"""
from typing import List, Dict, Any

class TradeoffAnalyzer:
    @staticmethod
    def identify_pareto_optimal_initiatives(
        initiatives: List[Dict[str, Any]],  # name, cost, risk_reduction, weeks
    ) -> List[Dict[str, Any]]:
        """Identifies non-dominated initiatives along Pareto frontier."""
        pareto = []
        for i, cand in enumerate(initiatives):
            dominated = False
            for j, other in enumerate(initiatives):
                if i != j:
                    # other dominates cand if cost <= and risk_reduction >= and at least one strictly better
                    if (
                        other["cost"] <= cand["cost"]
                        and other["risk_reduction"] >= cand["risk_reduction"]
                        and other["weeks"] <= cand["weeks"]
                        and (
                            other["cost"] < cand["cost"]
                            or other["risk_reduction"] > cand["risk_reduction"]
                            or other["weeks"] < cand["weeks"]
                        )
                    ):
                        dominated = True
                        break
            pareto.append({**cand, "is_pareto_optimal": not dominated})

        return sorted(pareto, key=lambda x: (not x["is_pareto_optimal"], -x["risk_reduction"]))
