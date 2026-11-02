from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.report_service import ReportAndDatasetService
from app.schemas.datasets import ModelIntelligenceItemSchema

router = APIRouter(prefix="/models", tags=["Model Registry & Intelligence"])

@router.get("", response_model=List[ModelIntelligenceItemSchema])
def list_models(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List registered machine learning models, training versions, accuracy, and drift status."""
    return ReportAndDatasetService.get_models(db, user.organization_id)
