"""AEGIS Model Intelligence & MLOps Registry API Router."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.datasets import MLModelItemSchema
from app.mlops.model_registry import ModelRegistryService

router = APIRouter(prefix="/models", tags=["MLOps & Model Intelligence"])

@router.get("", response_model=List[MLModelItemSchema])
@router.get("/", response_model=List[MLModelItemSchema])
def list_models(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists registered production machine learning models and validation metrics."""
    return IntelligenceService.get_models(db, user.organization_id)

@router.get("/governance-registry")
def list_governance_models(user: User = Depends(get_current_user)):
    """Returns champion/challenger model versions with training artifacts."""
    return ModelRegistryService.list_registered_models()
