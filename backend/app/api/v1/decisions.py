from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.decisions import DecisionItemSchema, DecisionApprovalResponse

router = APIRouter(prefix="/decisions", tags=["Decision Intelligence"])

@router.get("", response_model=List[DecisionItemSchema])
def list_decisions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve actionable, evidence-backed decision recommendations."""
    return IntelligenceService.get_decisions(db, user.organization_id)

@router.post("/{decision_id}/approve", response_model=DecisionApprovalResponse)
def approve_decision(decision_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Authorize a human-in-the-loop executive decision approval."""
    return IntelligenceService.approve_decision(db, user.organization_id, decision_id)

@router.post("/{decision_id}/reject", response_model=DecisionApprovalResponse)
def reject_decision(decision_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Reject or dismiss a suggested recommendation."""
    return DecisionApprovalResponse(
        success=True,
        message=f"Decision '{decision_id}' dismissed by user.",
    )
