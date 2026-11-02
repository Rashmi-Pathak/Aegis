from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.report_service import ReportAndDatasetService
from app.schemas.reports import AlertItemSchema

router = APIRouter(prefix="/alerts", tags=["Real-Time Threat Alerts"])

@router.get("", response_model=List[AlertItemSchema])
def list_alerts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve active system and risk alerts."""
    return ReportAndDatasetService.get_alerts(db, user.organization_id)
