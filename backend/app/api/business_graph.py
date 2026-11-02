"""AEGIS Business Graph API Router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.graph import BusinessGraphData
from app.business_graph.centrality import GraphCentralityEngine
from app.business_graph.graph_builder import BusinessGraphBuilder

router = APIRouter(prefix="/graph", tags=["Business Dependency Digital Twin"])

@router.get("", response_model=BusinessGraphData)
@router.get("/", response_model=BusinessGraphData)
@router.get("/business-digital-twin", response_model=BusinessGraphData)
def get_graph(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve full NetworkX-calculated dependency graph nodes and edges."""
    return IntelligenceService.get_business_graph(db, user.organization_id)

@router.get("/centrality-bottlenecks")
def get_bottlenecks(user: User = Depends(get_current_user)):
    """Computes PageRank and Betweenness centrality choke points."""
    twin = BusinessGraphBuilder.create_default_primelogix_digital_twin()
    return GraphCentralityEngine.analyze_network_centrality(twin.graph)
