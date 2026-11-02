"""AEGIS Real-Time Alerts & Notification Center Router."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["Alerts & Escalations"])

@router.get("")
@router.get("/")
def list_alerts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns all active threat alerts and system warnings."""
    return IntelligenceService.get_alerts(db, user.organization_id)

@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Acknowledges an alert and transitions state."""
    db_alert = db.query(Alert).filter(Alert.id == alert_id, Alert.organization_id == user.organization_id).first()
    if db_alert:
        db_alert.acknowledged = True
        db.commit()
    return {"success": True, "alert_id": alert_id, "status": "ACKNOWLEDGED"}
