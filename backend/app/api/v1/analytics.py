from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.analytics import AnalyticsOverview

router = APIRouter(prefix="/analytics", tags=["Business Analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve full analytics overview with KPIs, revenue trend, and category breakdowns."""
    return IntelligenceService.get_analytics_overview(db, user.organization_id)

@router.get("/revenue")
def get_revenue_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve multi-period actual vs target revenue performance."""
    overview = IntelligenceService.get_analytics_overview(db, user.organization_id)
    return overview.revenueTrend

@router.get("/kpis")
def get_kpi_metrics(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve individual KPI metrics and trend indicators."""
    overview = IntelligenceService.get_analytics_overview(db, user.organization_id)
    return overview.kpis
