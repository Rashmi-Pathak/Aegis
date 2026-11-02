from typing import Dict, Any, List
import pandas as pd
import numpy as np

class DataProfiler:
    """Calculates comprehensive dataset profiling and real 0-100 data quality score."""

    @staticmethod
    def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """Profile a dataframe and calculate its data quality metrics."""
        total_rows = len(df)
        total_cols = len(df.columns)
        
        if total_rows == 0 or total_cols == 0:
            return {
                "quality_score": 100.0,
                "total_rows": 0,
                "total_cols": 0,
                "missing_rate": 0.0,
                "duplicate_rate": 0.0,
                "outlier_count": 0,
            }

        # 1. Missingness
        total_cells = total_rows * total_cols
        total_nulls = int(df.isna().sum().sum())
        missing_rate = float(total_nulls / total_cells)

        # 2. Duplicate rows
        duplicate_rows = int(df.duplicated().sum())
        duplicate_rate = float(duplicate_rows / total_rows)

        # 3. Numeric Outliers
        outlier_count = 0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            s = df[col].dropna()
            if len(s) > 10:
                q25 = s.quantile(0.25)
                q75 = s.quantile(0.75)
                iqr = q75 - q25
                if iqr > 0:
                    outliers = ((s < (q25 - 1.5 * iqr)) | (s > (q75 + 1.5 * iqr))).sum()
                    outlier_count += int(outliers)

        # 4. Data Quality Score formulation (0-100)
        # Completeness penalty: up to 40 pts
        completeness_score = max(0.0, 100.0 - (missing_rate * 250.0))
        # Uniqueness penalty: up to 30 pts
        uniqueness_score = max(0.0, 100.0 - (duplicate_rate * 300.0))
        # Outlier penalty: up to 30 pts
        outlier_rate = min(1.0, outlier_count / max(1, total_rows))
        validity_score = max(0.0, 100.0 - (outlier_rate * 100.0))

        overall_quality = round(0.45 * completeness_score + 0.30 * uniqueness_score + 0.25 * validity_score, 1)

        return {
            "quality_score": overall_quality,
            "total_rows": total_rows,
            "total_cols": total_cols,
            "missing_rate": round(missing_rate, 4),
            "duplicate_rate": round(duplicate_rate, 4),
            "outlier_count": outlier_count,
        }
