"""AEGIS Feature Store & Time-Travel Point-in-Time Join Engine
Manages engineered features, entity keys, and offline historical snapshots for reproducible ML training.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np


class FeatureStore:
    """Enterprise feature definitions and point-in-time consistent joins."""

    def __init__(self):
        self._feature_views: Dict[str, pd.DataFrame] = {}

    def register_feature_view(
        self,
        view_name: str,
        df: pd.DataFrame,
        entity_key: str,
        timestamp_col: str,
    ):
        """Stores a feature view with entity keys and observation timestamps."""
        clean_df = df.copy()
        clean_df[timestamp_col] = pd.to_datetime(clean_df[timestamp_col], errors="coerce")
        self._feature_views[view_name] = {
            "df": clean_df,
            "entity_key": entity_key,
            "timestamp_col": timestamp_col,
        }

    def get_point_in_time_features(
        self,
        observation_df: pd.DataFrame,
        entity_key: str,
        observation_time_col: str,
        feature_view_name: str,
        feature_columns: List[str],
    ) -> pd.DataFrame:
        """Executes point-in-time backward as-of join to avoid future target leakage."""
        if feature_view_name not in self._feature_views:
            return observation_df

        view = self._feature_views[feature_view_name]
        f_df = view["df"]
        f_time = view["timestamp_col"]

        obs = observation_df.copy()
        obs[observation_time_col] = pd.to_datetime(obs[observation_time_col])

        # As-of merge
        merged = pd.merge_asof(
            obs.sort_values(observation_time_col),
            f_df[[view["entity_key"], f_time] + feature_columns].sort_values(f_time),
            left_on=observation_time_col,
            right_on=f_time,
            by=entity_key,
            direction="backward",
        )

        return merged
