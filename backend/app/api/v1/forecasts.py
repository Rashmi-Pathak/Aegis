from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.forecasts import ForecastItemSchema

router = APIRouter(prefix="/forecasts", tags=["Predictive Telemetry & Forecasting"])

@router.get("", response_model=List[ForecastItemSchema])
def list_forecasts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve multi-horizon ensemble forecasts with confidence bounds and accuracy metrics."""
    return IntelligenceService.get_forecasts(db, user.organization_id)
