"""AEGIS Executive Reports & Governance Briefing API Router."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.report_service import ReportService
from app.schemas.reports import ReportItemSchema

router = APIRouter(prefix="/reports", tags=["Reports & Executive Briefings"])

@router.get("", response_model=List[ReportItemSchema])
@router.get("/", response_model=List[ReportItemSchema])
def list_reports(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists generated executive memos, risk audits, and board decks."""
    return ReportService.list_reports(db, user.organization_id)

@router.post("/generate")
def generate_report(report_type: str = Query(default="executive_briefing"), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generates a real-time markdown briefing grounded in current telemetry."""
    return ReportService.create_executive_briefing(db, user.organization_id)
