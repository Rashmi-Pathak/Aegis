"""AEGIS Multi-Horizon Forecasting API Router
Provides multi-period demand, revenue, and cash-flow forecasts with prediction bounds.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/forecasts", tags=["Forecasting"])

@router.get("")
@router.get("/")
def list_forecasts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns ensemble time-series forecasts with confidence bounds."""
    return IntelligenceService.get_forecasts(db, user.organization_id)
