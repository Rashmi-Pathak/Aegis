"""AEGIS MLOps Champion/Challenger Test Suite."""
import pytest
from app.mlops.champion_challenger import ChampionChallengerRouter

def test_champion_challenger_comparison():
    res = ChampionChallengerRouter.compare_inference(
        champion_model_id="iso_forest_v1",
        challenger_model_id="iso_forest_v2",
        ground_truth=100.0,
        champion_prediction=112.0,  # Error 12
        challenger_prediction=103.0, # Error 3 (much better)
    )
    assert res["challenger_outperformed"] is True
    assert res["promotion_recommendation"] == "PROMOTE_CHALLENGER"
    assert res["error_reduction_pct"] > 50.0
