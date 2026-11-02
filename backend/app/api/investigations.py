"""AEGIS Forensic Investigation & Root Cause Workspace Router."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.investigation.causal_trees import CausalTreeGenerator

router = APIRouter(prefix="/investigations", tags=["Forensic Investigations"])

@router.get("/tree")
def get_investigation_tree(symptom: str = Query(default="Operating Margin Compression"), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generates forensic 5-Whys causal tree connecting symptom to root triggers."""
    anomalies = IntelligenceService.get_anomalies(db, user.organization_id)
    drivers = [
        {"driver": "Diesel Spot Benchmark Squeeze", "attributionSharePct": 54.2},
        {"driver": "Port Dwell Delay Demurrage", "attributionSharePct": 28.5},
    ]
    return CausalTreeGenerator.generate_investigation_tree(symptom, anomalies, drivers)
