"""AEGIS Ingestion Loaders & Delimiter Sniffing Test Suite."""
import pytest
import io
import pandas as pd
from app.ingestion.csv_loader import RobustCSVLoader
from app.ingestion.file_detector import FileTypeDetector

def test_semicolon_delimited_csv():
    content = "date;sales;region\n2025-01-01;500;EMEA\n2025-01-02;600;APAC\n".encode("utf-8")
    delim = RobustCSVLoader.sniff_delimiter(content)
    assert delim == ";"
    df = RobustCSVLoader.load_dataframe(content)
    assert len(df) == 2
    assert "sales" in df.columns

def test_tab_delimited_csv():
    content = "id\tmetric\tval\n1\tcost\t12.5\n2\trev\t25.0\n".encode("utf-8")
    delim = RobustCSVLoader.sniff_delimiter(content)
    assert delim == "\t"
    df = RobustCSVLoader.load_dataframe(content)
    assert len(df) == 2

def test_file_type_magic_bytes():
    zip_bytes = b"PK\x03\x04\x14\x00\x00\x00..."
    assert FileTypeDetector.detect_format(zip_bytes, "data.zip") == "zip"
    assert FileTypeDetector.detect_format(zip_bytes, "workbook.xlsx") == "xlsx"
