"""AEGIS Data Quality & Completeness Diagnostics
Audits missingness patterns, null thresholds, schema conforming rates, and record densities.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


class DataQualityAuditor:
    """Profiles incoming dataset completeness and health."""

    @staticmethod
    def audit_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates multi-dimensional completeness score (0-100)."""
        if df.empty:
            return {"quality_score": 0.0, "total_records": 0, "status": "EMPTY"}

        total_cells = df.size
        null_cells = int(df.isnull().sum().sum())
        completeness_pct = round(((total_cells - null_cells) / total_cells) * 100.0, 1)

        # Duplicate check
        duplicate_rows = int(df.duplicated().sum())
        uniqueness_pct = round(((len(df) - duplicate_rows) / len(df)) * 100.0, 1) if len(df) > 0 else 100.0

        # Column profile
        column_health = []
        for col in df.columns:
            col_nulls = int(df[col].isnull().sum())
            col_total = len(df)
            col_comp = round(((col_total - col_nulls) / col_total) * 100.0, 1)
            column_health.append({
                "column": str(col),
                "completeness_pct": col_comp,
                "missing_count": col_nulls,
                "data_type": str(df[col].dtype),
            })

        overall_score = round((completeness_pct * 0.7) + (uniqueness_pct * 0.3), 1)

        return {
            "overall_quality_score": overall_score,
            "total_records": len(df),
            "total_columns": len(df.columns),
            "missing_cells": null_cells,
            "duplicate_records": duplicate_rows,
            "completeness_percentage": completeness_pct,
            "uniqueness_percentage": uniqueness_pct,
            "column_profiles": column_health,
        }
