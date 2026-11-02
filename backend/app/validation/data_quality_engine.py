"""AEGIS Unified Data Quality Scoring Engine
Computes comprehensive dataset quality grades across completeness, validity, uniqueness, and consistency.
"""
from typing import Dict, Any
import pandas as pd
from app.data_quality.completeness import DataQualityAuditor

class UnifiedDataQualityEngine:
    @classmethod
    def evaluate_dataset(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """Runs audit and assigns letter grade (A+, A, B, C, F)."""
        audit = DataQualityAuditor.audit_dataframe(df)
        score = audit["overall_quality_score"]

        if score >= 95.0:
            grade = "A+"
        elif score >= 88.0:
            grade = "A"
        elif score >= 75.0:
            grade = "B"
        elif score >= 60.0:
            grade = "C"
        else:
            grade = "F"

        return {
            **audit,
            "quality_grade": grade,
            "is_production_ready": bool(score >= 75.0),
        }
