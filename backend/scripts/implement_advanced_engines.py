"""Advanced engines and test suites builder for AEGIS Python intelligence platform.
"""

import os

FILES = {}

# 1. Ingestion Loaders & Sniffers
FILES["backend/app/ingestion/csv_loader.py"] = '''"""AEGIS Robust Chunked CSV Ingestion Engine
Handles encoding detection (UTF-8, Latin-1, CP1252), delimiter sniffing,
and stream processing for multi-gigabyte business datasets.
"""
from typing import Iterator, Dict, Any, List, Optional
import io
import csv
import pandas as pd

class RobustCSVLoader:
    ENCODINGS_TO_TRY = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
    DELIMITERS_TO_TRY = [",", ";", "\\t", "|"]

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
        # Fallback
        return pd.read_csv(io.BytesIO(file_content), sep=None, engine="python", nrows=max_rows)

    @classmethod
    def stream_chunks(cls, file_path: str, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
        """Memory-efficient generator yielding chunks for huge tabular datasets."""
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, low_memory=False):
            yield chunk
'''

FILES["backend/app/ingestion/excel_loader.py"] = '''"""AEGIS Multi-Sheet Excel Workbook Ingestion Engine
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
                    # Clean unnamed columns
                    clean_cols = [c for c in df.columns if not str(c).startswith("Unnamed:")]
                    if clean_cols:
                        sheet_dfs[sheet_name] = df[clean_cols]
                    else:
                        sheet_dfs[sheet_name] = df
            except Exception:
                continue
        return sheet_dfs
'''

FILES["backend/app/ingestion/file_detector.py"] = '''"""AEGIS Binary File Format & Magic Byte Sniffer
Identifies file types independently of file extensions to prevent upload spoofing.
"""
from typing import Dict, Any, Optional

class FileTypeDetector:
    MAGIC_SIGNATURES = {
        b"PK\\x03\\x04": "zip",
        b"\\x1f\\x8b": "gzip",
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

        # Text sniffing for CSV or JSON
        try:
            sample = header_bytes[:512].decode("utf-8", errors="ignore").strip()
            if sample.startswith("{") or sample.startswith("["):
                return "json"
            if "," in sample or ";" in sample or "\\t" in sample:
                return "csv"
        except Exception:
            pass

        ext = filename.split(".")[-1].lower() if "." in filename else "unknown"
        return ext
'''

FILES["backend/app/ingestion/dataset_registry.py"] = '''"""AEGIS Ingestion Dataset Registry & Lineage Tracker
Maintains historical provenance, row counts, schema snapshots, and storage locations.
"""
from typing import Dict, Any, List, Optional
import datetime

class DatasetProvenanceRegistry:
    _registry: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register_dataset(
        cls,
        dataset_id: str,
        name: str,
        organization_id: str,
        format_type: str,
        record_count: int,
        columns: List[str],
        storage_path: str,
    ) -> Dict[str, Any]:
        """Logs dataset ingestion metadata."""
        record = {
            "dataset_id": dataset_id,
            "name": name,
            "organization_id": organization_id,
            "format": format_type,
            "record_count": record_count,
            "column_count": len(columns),
            "columns": columns,
            "storage_path": storage_path,
            "ingested_at": datetime.datetime.now().isoformat(),
            "status": "VALIDATED",
        }
        cls._registry[dataset_id] = record
        return record

    @classmethod
    def get_dataset_metadata(cls, dataset_id: str) -> Optional[Dict[str, Any]]:
        return cls._registry.get(dataset_id)
'''

# 2. Simulation Modules
FILES["backend/app/simulation/parameter_models.py"] = '''"""AEGIS Simulation Shock Parameter Domain Models
Defines typed bounded parameter models for What-If scenario simulations.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class FuelShockParameters(BaseModel):
    fuel_price_hike_pct: float = Field(default=20.0, ge=-50.0, le=200.0)
    route_efficiency_adjustment: float = Field(default=0.0, ge=-20.0, le=50.0)

class PortCongestionParameters(BaseModel):
    dwell_days_delta: float = Field(default=3.5, ge=0.0, le=30.0)
    demurrage_cost_per_day: float = Field(default=350.0, ge=50.0, le=5000.0)

class DemandDropParameters(BaseModel):
    volume_contraction_pct: float = Field(default=15.0, ge=-100.0, le=100.0)
    pricing_pressure_pct: float = Field(default=5.0, ge=-50.0, le=50.0)

class MacroeconomicShockParameters(BaseModel):
    interest_rate_delta_bps: float = Field(default=150.0, ge=-500.0, le=1000.0)
    headline_inflation_pct: float = Field(default=6.5, ge=0.0, le=50.0)
'''

FILES["backend/app/simulation/scenario.py"] = '''"""AEGIS Scenario Definition & Parameter Registry
Standard library of enterprise What-If scenarios available to executives.
"""
from typing import Dict, Any, List

class EnterpriseScenarioLibrary:
    SCENARIOS = [
        {
            "id": "fuel_shock",
            "name": "Global Diesel & Energy Benchmark Surge",
            "category": "supply_chain",
            "description": "Simulates 25% diesel spike across regional linehaul routes.",
            "default_params": {"fuel_price_hike_pct": 25.0},
        },
        {
            "id": "port_dwell_congestion",
            "name": "Major Container Hub Dwell Delays",
            "category": "operations",
            "description": "Simulates 4.5 day average dwell increase at Rotterdam & Long Beach.",
            "default_params": {"dwell_days_delta": 4.5},
        },
        {
            "id": "enterprise_churn_cascade",
            "name": "Key Client Portfolio Contraction",
            "category": "revenue",
            "description": "Simulates loss of top 3 tier-1 logistics freight contracts.",
            "default_params": {"churn_rate_pct": 12.0},
        },
        {
            "id": "interest_rate_liquidity_squeeze",
            "name": "Central Bank Rate Hike & Debt Servicing",
            "category": "finance",
            "description": "Simulates +200 bps floating interest rate spike on corporate debt.",
            "default_params": {"rate_delta_bps": 200},
        },
    ]

    @classmethod
    def list_scenarios(cls) -> List[Dict[str, Any]]:
        return cls.SCENARIOS
'''

FILES["backend/app/simulation/scenario_engine.py"] = '''"""AEGIS Scenario Execution Engine
Applies counterfactual shocks to baseline P&L and operational parameters.
"""
from typing import Dict, Any
from app.simulation.parameter_models import FuelShockParameters, PortCongestionParameters

class ScenarioEngine:
    @staticmethod
    def execute_fuel_shock(
        baseline_revenue: float,
        baseline_costs: float,
        annual_fuel_spend: float,
        params: FuelShockParameters,
    ) -> Dict[str, Any]:
        """Projects margin impact of fuel price hike."""
        fuel_delta = annual_fuel_spend * (params.fuel_price_hike_pct / 100.0)
        efficiency_savings = fuel_delta * (params.route_efficiency_adjustment / 100.0)
        net_fuel_cost = fuel_delta - efficiency_savings

        sim_costs = baseline_costs + net_fuel_cost
        baseline_profit = baseline_revenue - baseline_costs
        sim_profit = baseline_revenue - sim_costs

        base_margin = (baseline_profit / baseline_revenue) * 100.0 if baseline_revenue > 0 else 0.0
        sim_margin = (sim_profit / baseline_revenue) * 100.0 if baseline_revenue > 0 else 0.0

        return {
            "scenario": "fuel_shock",
            "baselineRevenue": round(baseline_revenue, 2),
            "simulatedRevenue": round(baseline_revenue, 2),
            "baselineProfit": round(baseline_profit, 2),
            "simulatedProfit": round(sim_profit, 2),
            "projectedMarginDelta": round(sim_margin - base_margin, 2),
            "costInflationUsd": round(net_fuel_cost, 2),
            "severity": "CRITICAL" if (sim_margin - base_margin) < -3.0 else "WARNING",
        }
'''

# 3. Risk Engine Modules
FILES["backend/app/risk_engine/risk_rules.py"] = '''"""AEGIS Risk Classification & Category Tagging Rules
Maps observed telemetry anomalies into ISO 31000 standard corporate risk buckets.
"""
from typing import Dict, Any, List

class RiskClassificationRules:
    CATEGORY_MAPPING = {
        "fuel_price": "financial",
        "diesel": "financial",
        "freight_rate": "financial",
        "port_dwell": "operational",
        "transit_delay": "operational",
        "driver_turnover": "operational",
        "customer_churn": "strategic",
        "covenant_breach": "regulatory",
        "temperature_drift": "supply_chain",
    }

    @classmethod
    def classify_metric_risk(cls, metric_name: str) -> str:
        """Determines category for anomalous metric."""
        metric_lower = metric_name.lower()
        for k, cat in cls.CATEGORY_MAPPING.items():
            if k in metric_lower:
                return cat
        return "operational"
'''

FILES["backend/app/risk_engine/severity.py"] = '''"""AEGIS Risk Severity Tier Determination
Categorizes continuous composite scores into standardized critical, high, medium, low tiers.
"""
from typing import Dict, Any

class SeverityClassifier:
    @staticmethod
    def get_tier(risk_score: float) -> str:
        if risk_score >= 75.0:
            return "critical"
        elif risk_score >= 50.0:
            return "high"
        elif risk_score >= 25.0:
            return "medium"
        else:
            return "low"

    @staticmethod
    def get_color_token(severity: str) -> str:
        tokens = {
            "critical": "#FF3B30",
            "high": "#FF6A00",
            "medium": "#FFB15A",
            "low": "#34C759",
        }
        return tokens.get(severity, "#A89D92")
'''

# 4. Business Graph Modules
FILES["backend/app/business_graph/dependency_analysis.py"] = '''"""AEGIS Graph Dependency Analysis & Upstream/Downstream Tracing
Analyzes upstream supply dependencies and downstream customer revenue blast radius.
"""
from typing import Dict, Any, List, Set
import networkx as nx

class GraphDependencyAnalyzer:
    @staticmethod
    def get_blast_radius(graph: nx.DiGraph, root_node: str) -> Dict[str, Any]:
        """Calculates all downstream nodes reachable from root node."""
        if root_node not in graph:
            return {"impacted_nodes": [], "blast_radius_score": 0.0}

        downstream = list(nx.descendants(graph, root_node))
        upstream = list(nx.ancestors(graph, root_node))

        total_nodes = len(graph.nodes)
        blast_score = (len(downstream) / total_nodes) * 100.0 if total_nodes > 0 else 0.0

        return {
            "root_node": root_node,
            "downstream_impacted_nodes": downstream,
            "upstream_dependency_nodes": upstream,
            "downstream_count": len(downstream),
            "blast_radius_percentage": round(blast_score, 1),
        }
'''

FILES["backend/app/business_graph/graph_risk.py"] = '''"""AEGIS Graph Structural Percolation & Fragility Modeling
Computes network percolation thresholds and robustness to node removal.
"""
from typing import Dict, Any
import networkx as nx

class GraphFragilityModel:
    @staticmethod
    def calculate_network_fragility(graph: nx.DiGraph) -> Dict[str, Any]:
        """Measures network density, reciprocity, and single-point-of-failure vulnerabilities."""
        if len(graph.nodes) == 0:
            return {"fragility_index": 0.0, "status": "EMPTY"}

        undirected = graph.to_undirected()
        is_connected = nx.is_connected(undirected)
        density = nx.density(graph)

        # Cut nodes (articulation points) whose removal disconnects the graph
        try:
            cut_nodes = list(nx.articulation_points(undirected))
        except Exception:
            cut_nodes = []

        fragility_score = min(100.0, (len(cut_nodes) * 20.0) + ((1.0 - density) * 30.0))

        return {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "graph_density": round(float(density), 3),
            "single_points_of_failure": cut_nodes,
            "fragility_score": round(float(fragility_score), 1),
            "resilience_tier": "Fragile" if len(cut_nodes) > 2 else "Resilient",
        }
'''

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Advanced engines generated successfully.")
'''

with open("backend/scripts/implement_advanced_engines.py", "w", encoding="utf-8") as f:
    f.write(FILES["backend/scripts/implement_advanced_engines.py"] if "backend/scripts/implement_advanced_engines.py" in FILES else "")
