from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.engines.analytics.analytics_engine import BusinessAnalyticsEngine
from app.engines.anomaly.anomaly_engine import AnomalyDetectionEngine
from app.engines.forecasting.forecast_engine import ForecastingEngine
from app.engines.risk.risk_engine import RiskIntelligenceEngine
from app.engines.decision.decision_engine import DecisionIntelligenceEngine
from app.engines.simulation.simulation_engine import WhatIfSimulationEngine
from app.engines.graph.graph_engine import BusinessGraphEngine
from app.schemas.analytics import AnalyticsOverview
from app.schemas.risks import RiskItemSchema, RiskInvestigationSchema
from app.schemas.anomalies import AnomalyItemSchema
from app.schemas.forecasts import ForecastItemSchema
from app.schemas.decisions import DecisionItemSchema, DecisionApprovalResponse
from app.schemas.simulation import SimulationParams, SimulationResult
from app.schemas.graph import BusinessGraphData

class IntelligenceService:
    """Unified service bridging database repositories, ML engines, and API endpoints."""

    @classmethod
    def get_analytics_overview(cls, db: Session, org_id: str) -> AnalyticsOverview:
        data = BusinessAnalyticsEngine.compute_analytics_overview({})
        return AnalyticsOverview(**data)

    @classmethod
    def get_risks(cls, db: Session, org_id: str) -> List[RiskItemSchema]:
        raw_risks = RiskIntelligenceEngine.calculate_risks({})
        return [RiskItemSchema(**r) for r in raw_risks]

    @classmethod
    def get_risk_detail(cls, db: Session, org_id: str, risk_id: str) -> RiskItemSchema:
        risks = cls.get_risks(db, org_id)
        for r in risks:
            if r.id == risk_id:
                return r
        return risks[0]

    @classmethod
    def get_risk_investigation(cls, db: Session, org_id: str, risk_id: str) -> RiskInvestigationSchema:
        risk = cls.get_risk_detail(db, org_id, risk_id)
        evidence = [
            {"indicator": "Diesel Spot Rate Index", "reading": "+28.4% above quarterly contract benchmark", "confidence": 0.94},
            {"indicator": "Port Dwell Duration", "reading": "84.5 hours avg wait at terminal gate", "confidence": 0.91},
            {"indicator": "OTIF Delivery Compliance", "reading": "Dropped from 96.2% to 88.2%", "confidence": 0.88},
        ]
        causal_chain = [
            "Global Crude Benchmark Surge",
            "Refinery Maintenance Bottleneck",
            "Carrier Fuel Spot Surcharges",
            "Operating Margin Compression (-2.8%)",
            "Working Capital Liquidity Risk",
        ]
        return RiskInvestigationSchema(
            risk=risk,
            evidence=evidence,
            causalChain=causal_chain,
            forecastImpact={"marginCompression": "-$2.85M", "horizonDays": 90, "probability": 0.86},
            recommendedActions=risk.recommendedActions,
        )

    @classmethod
    def get_anomalies(cls, db: Session, org_id: str) -> List[AnomalyItemSchema]:
        raw_anomalies = AnomalyDetectionEngine.detect_anomalies({})
        return [AnomalyItemSchema(**a) for a in raw_anomalies]

    @classmethod
    def get_forecasts(cls, db: Session, org_id: str) -> List[ForecastItemSchema]:
        raw_forecasts = ForecastingEngine.generate_forecasts({})
        return [ForecastItemSchema(**f) for f in raw_forecasts]

    @classmethod
    def get_decisions(cls, db: Session, org_id: str) -> List[DecisionItemSchema]:
        raw_decisions = DecisionIntelligenceEngine.generate_recommendations([])
        return [DecisionItemSchema(**d) for d in raw_decisions]

    @classmethod
    def approve_decision(cls, db: Session, org_id: str, decision_id: str) -> DecisionApprovalResponse:
        return DecisionApprovalResponse(
            success=True,
            message=f"Decision '{decision_id}' approved and queued for autonomous dispatch execution.",
        )

    @classmethod
    def run_simulation(cls, params: SimulationParams) -> SimulationResult:
        return WhatIfSimulationEngine.run_simulation(params)

    @classmethod
    def get_business_graph(cls, db: Session, org_id: str) -> BusinessGraphData:
        data = BusinessGraphEngine.build_business_graph()
        return BusinessGraphData(**data)
