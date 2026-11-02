from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.risks import RiskItemSchema, RiskInvestigationSchema

router = APIRouter(prefix="/risks", tags=["Risk Intelligence"])

@router.get("", response_model=List[RiskItemSchema])
def list_risks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List all detected enterprise risk exposure vectors."""
    return IntelligenceService.get_risks(db, user.organization_id)

@router.get("/{risk_id}", response_model=RiskItemSchema)
def get_risk_detail(risk_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get single risk breakdown."""
    return IntelligenceService.get_risk_detail(db, user.organization_id, risk_id)

@router.get("/{risk_id}/investigation", response_model=RiskInvestigationSchema)
def get_risk_investigation(risk_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Open deep causal investigation workspace for a given risk."""
    return IntelligenceService.get_risk_investigation(db, user.organization_id, risk_id)
