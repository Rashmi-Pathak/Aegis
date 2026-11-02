"""AEGIS End-to-End Enterprise Intelligence Pipeline Integration Test
Tests complete lifecycle: Raw Ingestion -> Profiling -> Canonical Mapping ->
Anomaly Detection -> Forecasting -> Risk Scoring -> Causal Investigation ->
Decision Optimization -> Executive Briefing.
"""
import pytest
import pandas as pd
import numpy as np

from app.ingestion.csv_loader import RobustCSVLoader
from app.ingestion.file_detector import FileTypeDetector
from app.data_quality.completeness import DataQualityAuditor
from app.canonical.field_mapper import SemanticFieldMapper
from app.anomaly_detection.isolation_forest import IsolationForestDetector
from app.forecasting.time_series import ClassicalForecaster
from app.risk_engine.scoring import RiskScorer
from app.business_graph.graph_builder import BusinessGraphBuilder
from app.business_graph.centrality import GraphCentralityEngine
from app.decision_engine.optimization import DecisionOptimizer
from app.reporting.executive_summary_generator import ExecutiveBriefingGenerator

def test_complete_intelligence_pipeline_lifecycle():
    # 1. Ingestion: Raw CSV content
    raw_csv = (
        "date,revenue,cost_of_sales,operating_expenses,shipment_count\n"
        "2025-01-01,100000,60000,20000,120\n"
        "2025-02-01,105000,62000,21000,125\n"
        "2025-03-01,110000,64000,21500,132\n"
        "2025-04-01,108000,63000,22000,128\n"
        "2025-05-01,115000,66000,22500,138\n"
        "2025-06-01,120000,95000,35000,145\n"  # Anomaly: cost spike
    ).encode("utf-8")

    fmt = FileTypeDetector.detect_format(raw_csv, "enterprise_data.csv")
    assert fmt == "csv"

    df = RobustCSVLoader.load_dataframe(raw_csv)
    assert len(df) == 6
    assert "revenue" in df.columns

    # 2. Data Quality Profiling
    quality = DataQualityAuditor.audit_dataframe(df)
    assert quality["overall_quality_score"] > 80.0

    # 3. Canonical Field Mapping
    mapped_cols = {col: SemanticFieldMapper.map_column(col) for col in df.columns}
    assert mapped_cols["cost_of_sales"] == "cogs"
    assert mapped_cols["revenue"] == "revenue"

    # 4. Anomaly Detection on Costs
    iso = IsolationForestDetector(contamination=0.15)
    iso_res = iso.fit_predict(df[["cost_of_sales", "operating_expenses"]])
    assert iso_res["outlier_count"] >= 1

    # 5. Forecasting Revenue
    rev_forecast = ClassicalForecaster.double_exponential_smoothing(df["revenue"].tolist(), horizon=3)
    assert len(rev_forecast["forecast"]) == 3
    assert rev_forecast["forecast"][-1] > 115000.0

    # 6. Quantitative Risk Scoring
    risk = RiskScorer.calculate_risk_score(
        probability=0.88,
        financial_impact_score=85.0,
        velocity_multiplier=1.2,
    )
    assert risk["severity"] == "critical"

    # 7. Business Dependency Digital Twin
    twin = BusinessGraphBuilder.create_default_primelogix_digital_twin()
    centrality = GraphCentralityEngine.analyze_network_centrality(twin.graph)
    assert len(centrality["top_bottlenecks"]) > 0

    # 8. Decision Optimization Levers
    instruments = [
        {"name": "Diesel Forward Contract", "cost_per_unit": 10000.0, "risk_mitigated_per_unit": 25.0, "max_units": 4},
        {"name": "Spot Rate Dynamic Buffer", "cost_per_unit": 4000.0, "risk_mitigated_per_unit": 8.0, "max_units": 5},
    ]
    allocation = DecisionOptimizer.allocate_hedging_budget(total_budget=30000.0, hedging_instruments=instruments)
    assert allocation["total_risk_points_reduced"] > 50.0

    # 9. Executive Intelligence Briefing
    briefing = ExecutiveBriefingGenerator.generate_briefing(
        organization_name="PrimeLogix Global Logistics",
        health_score=78.5,
        critical_risks=[{"title": "Fuel Spike Shock", "score": risk["risk_score"], "category": "Supply Chain"}],
        financial_kpis={"revenue": "$148.2M", "operatingMargin": "14.2%"},
        top_recommendations=[{"title": "Hedge Diesel via Forward Swaps", "roi_ratio": 3.8}],
    )
    assert "AEGIS EXECUTIVE RISK INTELLIGENCE BRIEFING" in briefing["markdown_content"]
    assert briefing["status"] == "APPROVED_FOR_DISTRIBUTION"
