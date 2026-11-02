from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.graph import BusinessGraphData

router = APIRouter(prefix="/graph", tags=["Business Dependency Digital Twin"])

@router.get("", response_model=BusinessGraphData)
@router.get("/", response_model=BusinessGraphData)
@router.get("/business-digital-twin", response_model=BusinessGraphData)
def get_business_graph(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve full NetworkX-calculated dependency graph nodes and edges."""
    return IntelligenceService.get_business_graph(db, user.organization_id)
