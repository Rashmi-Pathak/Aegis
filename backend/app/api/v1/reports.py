from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.report_service import ReportAndDatasetService
from app.schemas.reports import ReportItemSchema, AlertItemSchema

router = APIRouter(prefix="/reports", tags=["Executive Reports"])

@router.get("", response_model=List[ReportItemSchema])
def list_reports(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List available intelligence briefing reports."""
    return ReportAndDatasetService.get_reports(db, user.organization_id)
