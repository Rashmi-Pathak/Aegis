"""AEGIS Admin System Diagnostics & Health Router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.admin.system_service import AdminSystemDiagnostics

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

@router.get("/system-health")
def get_system_health(user: User = Depends(get_current_user)):
    """System health telemetry for admin operations console."""
    return AdminSystemDiagnostics.gather_system_metrics()
