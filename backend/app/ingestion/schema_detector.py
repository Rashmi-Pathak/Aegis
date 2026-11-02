from typing import Dict, Any, List
import pandas as pd
import numpy as np

class SchemaDetector:
    """Automatically analyzes heterogeneous business dataframes and detects types and relationships."""

    @staticmethod
    def detect_column_type(series: pd.Series) -> str:
        """Infer canonical business data type for a Pandas Series."""
        clean_series = series.dropna()
        if len(clean_series) == 0:
            return "VARCHAR"

        # 1. Datetime / Date checks
        col_name = str(series.name).lower()
        if any(w in col_name for w in ["date", "time", "timestamp", "created_at", "updated_at"]):
            try:
                pd.to_datetime(clean_series.iloc[:50], errors="raise")
                return "TIMESTAMP"
            except Exception:
                pass

        # 2. Boolean
        if set(clean_series.unique()).issubset({True, False, 0, 1, "0", "1", "true", "false", "True", "False"}):
            return "BOOLEAN"

        # 3. Numeric checks
        if pd.api.types.is_integer_dtype(series):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(series):
            if any(w in col_name for w in ["price", "cost", "revenue", "amount", "fee", "margin", "usd", "inr"]):
                return "DECIMAL(12,2)"
            return "FLOAT"

        # 4. UUID / ID checks
        if any(w in col_name for w in ["id", "uuid", "vin", "sku", "code"]):
            return "VARCHAR(64)"

        return "VARCHAR(255)"

    @classmethod
    def detect_schema(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Return list of schema field descriptors for a dataframe."""
        fields = []
        for col in df.columns:
            s = df[col]
            null_pct = round(float(s.isna().mean() * 100), 2)
            detected_type = cls.detect_column_type(s)

            # Check for numeric outliers via IQR
            has_outliers = False
            if pd.api.types.is_numeric_dtype(s) and len(s.dropna()) > 10:
                q25 = s.quantile(0.25)
                q75 = s.quantile(0.75)
                iqr = q75 - q25
                if iqr > 0:
                    outliers_count = ((s < (q25 - 1.5 * iqr)) | (s > (q75 + 1.5 * iqr))).sum()
                    has_outliers = bool(outliers_count > 0)

            fields.append({
                "name": str(col),
                "type": detected_type,
                "nullPercentage": null_pct,
                "hasOutliers": has_outliers,
            })
        return fields
