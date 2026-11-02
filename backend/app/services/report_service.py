from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.schemas.reports import ReportItemSchema, AlertItemSchema
from app.schemas.datasets import DatasetItemSchema, ModelIntelligenceItemSchema

class ReportAndDatasetService:
    """Manages reports, alerts, datasets, and registered ML models."""

    @classmethod
    def get_reports(cls, db: Session, org_id: str) -> List[ReportItemSchema]:
        return [
            ReportItemSchema(
                id="rep_exec_q1",
                title="Executive Risk & Capital Intelligence Briefing",
                category="executive",
                generatedAt="Today, 06:00 UTC",
                frequency="weekly",
                status="ready",
                summary="Synthesis of cross-business margins, exposure vectors, diesel hedging recommendation, and 90-day cash flow scenario.",
            ),
            ReportItemSchema(
                id="rep_fuel_surge",
                title="Commodity & Energy Price Exposure Audit",
                category="risk",
                generatedAt="Yesterday, 18:30 UTC",
                frequency="on_demand",
                status="ready",
                summary="Causal propagation analysis from crude futures into carrier spot surcharges and SLA penalties.",
            ),
            ReportItemSchema(
                id="rep_forecast_q2",
                title="90-Day Multi-Horizon Demand & Fleet Capacity Forecast",
                category="forecast",
                generatedAt="2 days ago",
                frequency="monthly",
                status="ready",
                summary="Trained ensemble models predicting lane-level freight demand, seasonal variance, and terminal storage capacity.",
            ),
            ReportItemSchema(
                id="rep_quality_mar",
                title="Canonical Data Quality & Ingestion Integrity Report",
                category="data_quality",
                generatedAt="3 days ago",
                frequency="weekly",
                status="ready",
                summary="Validation analysis across 8 enterprise datasets: 96.8% health score, 0 duplicate keys, 4 outlier records isolated.",
            ),
        ]

    @classmethod
    def get_alerts(cls, db: Session, org_id: str) -> List[AlertItemSchema]:
        return [
            AlertItemSchema(
                id="alt_01",
                timestamp="12m ago",
                severity="critical",
                source="Risk Engine - Energy Module",
                message="Fuel expense benchmark exceeded +15% alert threshold on Southwest corridor.",
                affectedMetric="Operating Margin ($2.85M Exposure)",
                actionRequired="Review Decision #DEC-01 (Rail Reroute)",
                isRead=False,
            ),
            AlertItemSchema(
                id="alt_02",
                timestamp="1h ago",
                severity="high",
                source="Anomaly Detector - Logistics EDI",
                message="Demurrage charges accelerated to $18.6K/day at Long Beach Terminal 4.",
                affectedMetric="Intermodal Dwell Fees",
                actionRequired="Trigger pre-clearance EDI customs expedite",
                isRead=False,
            ),
            AlertItemSchema(
                id="alt_03",
                timestamp="4h ago",
                severity="medium",
                source="Forecasting Engine",
                message="Q2 revenue confidence interval expanded to ±4.2% due to supplier pricing volatility.",
                affectedMetric="Revenue Predictability",
                actionRequired="Run What-If Scenario with +10% cost variance",
                isRead=True,
            ),
        ]

    @classmethod
    def get_datasets(cls, db: Session, org_id: str) -> List[DatasetItemSchema]:
        return [
            DatasetItemSchema(
                id="ds_freight_telemetry",
                name="Fleet IoT & GPS Telemetry Feed",
                sourceType="api",
                recordCount=284000,
                columnCount=18,
                qualityScore=98.0,
                lastUpdated="12m ago",
                status="ready",
                schema=[
                    {"name": "vehicle_vin", "type": "VARCHAR(17)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "timestamp", "type": "TIMESTAMP", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "speed_mph", "type": "FLOAT", "nullPercentage": 0.1, "hasOutliers": True},
                    {"name": "fuel_rate_gph", "type": "FLOAT", "nullPercentage": 0.4, "hasOutliers": True},
                    {"name": "engine_load_pct", "type": "FLOAT", "nullPercentage": 0.2, "hasOutliers": False},
                ],
            ),
            DatasetItemSchema(
                id="ds_tms_billing",
                name="TMS Shipping Orders & Invoicing",
                sourceType="postgres",
                recordCount=89400,
                columnCount=24,
                qualityScore=96.0,
                lastUpdated="1h ago",
                status="ready",
                schema=[
                    {"name": "order_id", "type": "UUID", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "client_id", "type": "VARCHAR(32)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "origin_hub", "type": "VARCHAR(8)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "dest_hub", "type": "VARCHAR(8)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "contract_rate_usd", "type": "DECIMAL(12,2)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "fuel_surcharge_usd", "type": "DECIMAL(10,2)", "nullPercentage": 1.2, "hasOutliers": True},
                ],
            ),
            DatasetItemSchema(
                id="ds_customs_edi",
                name="EDI-214 Carrier Shipment Status Messages",
                sourceType="zip",
                recordCount=54600,
                columnCount=14,
                qualityScore=94.0,
                lastUpdated="3h ago",
                status="ready",
                schema=[
                    {"name": "shipment_id", "type": "VARCHAR(32)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "status_code", "type": "VARCHAR(4)", "nullPercentage": 0.0, "hasOutliers": False},
                    {"name": "terminal_code", "type": "VARCHAR(8)", "nullPercentage": 0.8, "hasOutliers": False},
                    {"name": "dwell_hours", "type": "INTEGER", "nullPercentage": 0.0, "hasOutliers": True},
                ],
            ),
        ]

    @classmethod
    def get_models(cls, db: Session, org_id: str) -> List[ModelIntelligenceItemSchema]:
        return [
            ModelIntelligenceItemSchema(
                id="mdl_revenue_ensemble",
                name="Multi-Horizon Topline Forecast (LightGBM + ARIMA)",
                type="forecasting",
                version="v2.4.1",
                accuracy="97.2%",
                mae="$0.28M",
                rmse="$0.41M",
                driftStatus="stable",
                lastTrained="Yesterday, 02:00 UTC",
            ),
            ModelIntelligenceItemSchema(
                id="mdl_iforest_anom",
                name="Isolation Forest Outlier Detector (Contamination=0.03)",
                type="anomaly",
                version="v3.1.0",
                accuracy="94.8%",
                mae="N/A",
                rmse="N/A",
                driftStatus="stable",
                lastTrained="3 days ago",
            ),
            ModelIntelligenceItemSchema(
                id="mdl_risk_propagation",
                name="NetworkX Causal Stress Wave Simulator",
                type="causal_graph",
                version="v1.8.2",
                accuracy="92.4%",
                mae="N/A",
                rmse="N/A",
                driftStatus="stable",
                lastTrained="1 week ago",
            ),
        ]
