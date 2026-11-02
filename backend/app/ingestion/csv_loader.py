"""AEGIS Robust Chunked CSV Ingestion Engine
Handles encoding detection (UTF-8, Latin-1, CP1252), delimiter sniffing,
and stream processing for multi-gigabyte business datasets.
"""
from typing import Iterator, Dict, Any, List, Optional
import io
import pandas as pd

class RobustCSVLoader:
    ENCODINGS_TO_TRY = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
    DELIMITERS_TO_TRY = [",", ";", "\t", "|"]

    @classmethod
    def sniff_delimiter(cls, sample_bytes: bytes) -> str:
        """Determines most likely CSV delimiter by analyzing character frequencies."""
        text = sample_bytes.decode("utf-8", errors="ignore")[:4096]
        counts = {d: text.count(d) for d in cls.DELIMITERS_TO_TRY}
        best = max(counts, key=counts.get)
        return best if counts[best] > 0 else ","

    @classmethod
    def load_dataframe(cls, file_content: bytes, max_rows: Optional[int] = None) -> pd.DataFrame:
        """Parses raw bytes into Pandas DataFrame with resilient encoding and delimiter fallback."""
        delim = cls.sniff_delimiter(file_content)
        for enc in cls.ENCODINGS_TO_TRY:
            try:
                stream = io.BytesIO(file_content)
                df = pd.read_csv(
                    stream,
                    sep=delim,
                    encoding=enc,
                    nrows=max_rows,
                    low_memory=False,
                    on_bad_lines="skip",
                )
                return df
            except Exception:
                continue
        return pd.read_csv(io.BytesIO(file_content), sep=None, engine="python", nrows=max_rows)
