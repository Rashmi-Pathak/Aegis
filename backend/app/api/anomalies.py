"""AEGIS Anomaly Detection API Router
Provides endpoints for telemetry outlier detection, resolution, and status updates.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/anomalies", tags=["Anomaly Detection"])

@router.get("")
@router.get("/")
def list_anomalies(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists all active and unresolved anomalies across enterprise sensor and transaction streams."""
    return IntelligenceService.get_anomalies(db, user.organization_id)
