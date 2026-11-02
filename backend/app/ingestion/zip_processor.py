import os
import zipfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from app.core.exceptions import IngestionError
from app.core.logging import log_pipeline_event

class SecureZipProcessor:
    """Safely inspects and extracts enterprise business data ZIP archives."""
    
    MAX_FILE_SIZE_BYTES = 250 * 1024 * 1024  # 250MB
    MAX_TOTAL_EXTRACTED_BYTES = 1024 * 1024 * 1024  # 1GB limit
    MAX_ENTRIES_COUNT = 500

    @staticmethod
    def inspect_zip(zip_path: Path) -> Dict[str, Any]:
        """Inspect contents of zip without extracting to disk."""
        if not zip_path.exists():
            raise IngestionError(f"ZIP archive not found at: {zip_path}")
        
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                file_list = zf.namelist()
                company_meta = {}
                
                # Check for company.json
                for name in file_list:
                    if name.endswith("company.json") or name == "company.json":
                        with zf.open(name) as f:
                            company_meta = json.loads(f.read().decode("utf-8"))
                        break
                
                csv_files = [f for f in file_list if f.endswith(".csv")]
                
                return {
                    "zip_filename": zip_path.name,
                    "company_metadata": company_meta,
                    "all_files": file_list,
                    "csv_files": csv_files,
                    "dataset_count": len(csv_files),
                    "total_uncompressed_size": sum(zi.file_size for zi in zf.infolist()),
                }
        except Exception as e:
            raise IngestionError(f"Failed to inspect zip {zip_path.name}: {str(e)}")

    @classmethod
    def read_csv_from_zip(cls, zip_path: Path, csv_filename: str) -> pd.DataFrame:
        """Stream a CSV file directly from inside a zip archive into a Pandas DataFrame."""
        if not zip_path.exists():
            raise IngestionError(f"ZIP archive not found: {zip_path}")
        
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                # Find matching filename in zip entries
                matching = [n for n in zf.namelist() if n == csv_filename or n.endswith("/" + csv_filename)]
                if not matching:
                    raise IngestionError(f"CSV file '{csv_filename}' not found inside {zip_path.name}")
                
                with zf.open(matching[0]) as f:
                    df = pd.read_csv(f, low_memory=False)
                    return df
        except Exception as e:
            raise IngestionError(f"Error reading {csv_filename} from {zip_path.name}: {str(e)}")

    @classmethod
    def read_all_csvs_from_zip(cls, zip_path: Path) -> Dict[str, pd.DataFrame]:
        """Read all CSV files from a zip into memory as a dictionary of DataFrames."""
        info = cls.inspect_zip(zip_path)
        dataframes: Dict[str, pd.DataFrame] = {}
        
        for csv_name in info["csv_files"]:
            base_name = os.path.basename(csv_name).replace(".csv", "")
            try:
                df = cls.read_csv_from_zip(zip_path, csv_name)
                dataframes[base_name] = df
            except Exception as e:
                log_pipeline_event("CSV_READ_WARNING", f"Could not read {csv_name}: {str(e)}")
                
        return dataframes
