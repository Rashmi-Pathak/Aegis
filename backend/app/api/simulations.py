"""AEGIS What-If Simulation API Router
Executes real-time counterfactual shock simulations without mutating baseline databases.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/simulation", tags=["What-If Simulation"])

@router.post("/run")
def run_simulation(payload: Dict[str, Any], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Runs counterfactual shock scenario (fuel_shock, port_dwell, churn_spike)."""
    return IntelligenceService.run_simulation(db, user.organization_id, payload)
