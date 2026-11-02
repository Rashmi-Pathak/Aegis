"""AEGIS Multi-Sheet Excel Workbook Ingestion Engine
Extracts sheets, cleans header rows, and handles formulas.
"""
from typing import Dict, Any, List
import io
import pandas as pd

class ExcelWorkbookLoader:
    @staticmethod
    def inspect_and_load_sheets(file_content: bytes) -> Dict[str, pd.DataFrame]:
        """Loads all sheets from an .xlsx or .xls workbook into a dictionary of DataFrames."""
        stream = io.BytesIO(file_content)
        xl = pd.ExcelFile(stream)
        sheet_dfs = {}
        for sheet_name in xl.sheet_names:
            try:
                df = xl.parse(sheet_name)
                if not df.empty:
                    clean_cols = [c for c in df.columns if not str(c).startswith("Unnamed:")]
                    sheet_dfs[sheet_name] = df[clean_cols] if clean_cols else df
            except Exception:
                continue
        return sheet_dfs
