"""AEGIS MLOps Champion/Challenger Model Shadow Router
Routes incoming telemetry to both Champion (active) and Challenger (shadow) models
to benchmark inference accuracy and detect degradation before promotion.
"""
from typing import Dict, Any, List, Optional
import numpy as np

class ChampionChallengerRouter:
    @staticmethod
    def compare_inference(
        champion_model_id: str,
        challenger_model_id: str,
        ground_truth: float,
        champion_prediction: float,
        challenger_prediction: float,
    ) -> Dict[str, Any]:
        """Compares prediction error on actual outcome."""
        champ_err = abs(ground_truth - champion_prediction)
        chall_err = abs(ground_truth - challenger_prediction)

        challenger_outperformed = bool(chall_err < champ_err)
        margin_improvement_pct = ((champ_err - chall_err) / (champ_err or 1.0)) * 100.0

        return {
            "champion_id": champion_model_id,
            "challenger_id": challenger_model_id,
            "ground_truth": ground_truth,
            "champion_error": round(champ_err, 3),
            "challenger_error": round(chall_err, 3),
            "challenger_outperformed": challenger_outperformed,
            "error_reduction_pct": round(margin_improvement_pct, 2),
            "promotion_recommendation": "PROMOTE_CHALLENGER" if (challenger_outperformed and margin_improvement_pct > 15.0) else "RETAIN_CHAMPION",
        }
