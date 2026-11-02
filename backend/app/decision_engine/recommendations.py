"""AEGIS Multi-Objective Decision Trade-Off & Recommendation Engine
Ranks mitigation initiatives across Capital Cost, Risk Reduction, Implementation Time,
and ROI on Risk Mitigated.
"""

from typing import List, Dict, Any


class DecisionEngineLogic:
    """Evaluates mitigation candidates along Pareto frontiers."""

    @staticmethod
    def rank_mitigation_actions(
        initiatives: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Ranks actions by composite risk-adjusted ROI index."""
        ranked = []
        for item in initiatives:
            cost = max(1.0, item.get("capital_required", 10000.0))
            expected_loss_prevented = item.get("expected_loss_prevented", 50000.0)
            implementation_weeks = max(1, item.get("time_to_implement_weeks", 4))

            # ROI = (Loss Prevented - Cost) / Cost
            roi_ratio = round((expected_loss_prevented - cost) / cost, 2)

            # Velocity Score: faster execution yields higher operational agility
            agility_factor = 1.0 / (implementation_weeks ** 0.5)

            composite_score = round(roi_ratio * agility_factor * 10.0, 1)

            ranked.append({
                **item,
                "roi_ratio": roi_ratio,
                "composite_decision_score": composite_score,
                "payback_velocity": "Rapid (< 4 weeks)" if implementation_weeks <= 4 else "Strategic Quarterly",
            })

        return sorted(ranked, key=lambda x: x["composite_decision_score"], reverse=True)
