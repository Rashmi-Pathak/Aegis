"""AEGIS Root Cause Analysis & Diagnostic Attribution Engine
Isolates anomalous drivers using feature attribution and decision tree regression paths.
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor


class RootCauseAnalyzer:
    """Diagnoses the fundamental drivers of KPI degradation and operational breaks."""

    @staticmethod
    def identify_driver_importance(
        telemetry_df: pd.DataFrame,
        target_kpi_col: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Trains a shallow decision tree to identify which feature split causes largest variance."""
        if telemetry_df.empty or target_kpi_col not in telemetry_df.columns:
            return []

        numeric_df = telemetry_df.select_dtypes(include=[np.number]).dropna()
        if len(numeric_df) < 10 or target_kpi_col not in numeric_df.columns:
            return []

        X = numeric_df.drop(columns=[target_kpi_col])
        y = numeric_df[target_kpi_col]

        if X.empty:
            return []

        tree = DecisionTreeRegressor(max_depth=4, random_state=42)
        tree.fit(X, y)

        importances = tree.feature_importances_
        results = []
        for col, imp in zip(X.columns, importances):
            if imp > 0.01:
                results.append({
                    "driver": col,
                    "attributionSharePct": round(float(imp) * 100.0, 1),
                    "impactDirection": "Negative Drag" if float(np.corrcoef(X[col], y)[0, 1]) < 0 else "Positive Catalyst",
                })

        return sorted(results, key=lambda x: x["attributionSharePct"], reverse=True)[:top_k]
