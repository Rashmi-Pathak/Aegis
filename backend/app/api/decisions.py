"""AEGIS Decision Intelligence API Router
Provides prescriptive mitigation recommendations, ROI rankings, and approval governance workflows.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/decisions", tags=["Decision Intelligence"])

@router.get("")
@router.get("/")
def list_decisions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns ranked actionable interventions with projected risk-adjusted ROI."""
    return IntelligenceService.get_decisions(db, user.organization_id)
