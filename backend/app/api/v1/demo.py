from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from app.services.demo_service import DemoBusinessService
from app.schemas.datasets import DemoBusinessSchema

router = APIRouter(prefix="/demo", tags=["Demo Environments"])

@router.get("/businesses", response_model=List[DemoBusinessSchema])
def list_demo_businesses():
    """Discover all 15 synthetic enterprise ZIP archives dynamically from data/demo-businesses/."""
    return DemoBusinessService.discover_all_demo_businesses()

@router.get("/businesses/{business_id}", response_model=DemoBusinessSchema)
def get_demo_business(business_id: str):
    """Retrieve details for a specific demo business environment."""
    business = DemoBusinessService.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo business not found")
    return business

@router.get("/businesses/{business_id}/overview")
def get_demo_business_overview(business_id: str):
    """Retrieve operational telemetry snapshot for a demo business."""
    business = DemoBusinessService.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo business not found")
    return {
        "business": business,
        "healthScore": business["healthScore"],
        "activeRisks": business["riskCount"],
        "forecastConfidence": 0.94,
        "recentAnomalies": 3,
        "systemStatus": "OPERATIONAL",
    }

@router.post("/businesses/{business_id}/activate")
def activate_demo_business(business_id: str):
    """Activate the selected business environment for active tenant exploration."""
    business = DemoBusinessService.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo business not found")
    return {
        "success": True,
        "message": f"Demo environment '{business['name']}' activated successfully.",
        "businessId": business["id"],
    }
