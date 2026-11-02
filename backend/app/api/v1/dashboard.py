from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.services.report_service import ReportAndDatasetService

router = APIRouter(prefix="/dashboard", tags=["Command Center Dashboard"])

@router.get("/overview")
def get_dashboard_overview(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Executive Command Center aggregated operational overview."""
    analytics = IntelligenceService.get_analytics_overview(db, user.organization_id)
    risks = IntelligenceService.get_risks(db, user.organization_id)
    forecasts = IntelligenceService.get_forecasts(db, user.organization_id)
    decisions = IntelligenceService.get_decisions(db, user.organization_id)
    anomalies = IntelligenceService.get_anomalies(db, user.organization_id)
    alerts = ReportAndDatasetService.get_alerts(db, user.organization_id)

    return {
        "healthScore": analytics.healthScore,
        "kpis": analytics.kpis,
        "revenueTrend": analytics.revenueTrend,
        "activeRisks": risks,
        "criticalForecasts": forecasts,
        "pendingDecisions": decisions,
        "activeAnomalies": anomalies,
        "recentAlerts": alerts,
        "dataQualityScore": 96.0,
        "systemStatus": "OPERATIONAL",
    }
