from fastapi import APIRouter
from app.schemas.simulation import SimulationParams, SimulationResult
from app.services.intelligence_service import IntelligenceService

router = APIRouter(prefix="/simulation", tags=["What-If Simulation Engine"])

@router.post("/run", response_model=SimulationResult)
def run_what_if_simulation(params: SimulationParams):
    """Execute counterfactual scenario simulation without altering baseline production records."""
    return IntelligenceService.run_simulation(params)
