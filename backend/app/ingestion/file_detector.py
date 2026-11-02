"""AEGIS Binary File Format & Magic Byte Sniffer
Identifies file types independently of file extensions to prevent upload spoofing.
"""
from typing import Dict, Any, Optional

class FileTypeDetector:
    MAGIC_SIGNATURES = {
        b"PK\x03\x04": "zip",
        b"\x1f\x8b": "gzip",
        b"PAR1": "parquet",
        b"%PDF": "pdf",
    }

    @classmethod
    def detect_format(cls, header_bytes: bytes, filename: str = "") -> str:
        """Inspects first 16 bytes for magic signatures with extension fallback."""
        for sig, fmt in cls.MAGIC_SIGNATURES.items():
            if header_bytes.startswith(sig):
                if fmt == "zip" and (filename.endswith(".xlsx") or filename.endswith(".docx")):
                    return "xlsx" if filename.endswith(".xlsx") else "zip"
                return fmt

        try:
            sample = header_bytes[:512].decode("utf-8", errors="ignore").strip()
            if sample.startswith("{") or sample.startswith("["):
                return "json"
            if "," in sample or ";" in sample or "\t" in sample:
                return "csv"
        except Exception:
            pass

        ext = filename.split(".")[-1].lower() if "." in filename else "unknown"
        return ext
