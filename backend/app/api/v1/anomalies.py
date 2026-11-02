from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.anomalies import AnomalyItemSchema

router = APIRouter(prefix="/anomalies", tags=["Anomaly Detection"])

@router.get("", response_model=List[AnomalyItemSchema])
def list_anomalies(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List operational and financial statistical outliers detected across business metrics."""
    return IntelligenceService.get_anomalies(db, user.organization_id)
