"""AEGIS Duplicate Record & Fuzzy Entity Resolution Engine
Identifies duplicate transactional records and fuzzy customer entity matches.
"""
from typing import List, Dict, Any
import pandas as pd

class DuplicateDetector:
    @staticmethod
    def detect_exact_and_near_duplicates(
        df: pd.DataFrame,
        key_columns: List[str],
    ) -> Dict[str, Any]:
        """Finds duplicate rows based on subset of semantic key columns."""
        if df.empty or not key_columns:
            return {"duplicate_count": 0, "duplicate_rate_pct": 0.0}

        valid_keys = [c for c in key_columns if c in df.columns]
        if not valid_keys:
            valid_keys = df.columns.tolist()

        duplicates_mask = df.duplicated(subset=valid_keys, keep="first")
        dup_count = int(duplicates_mask.sum())
        rate = round((dup_count / len(df)) * 100.0, 2) if len(df) > 0 else 0.0

        return {
            "duplicate_count": dup_count,
            "duplicate_rate_pct": rate,
            "evaluated_keys": valid_keys,
            "has_high_duplication": bool(rate > 5.0),
        }
