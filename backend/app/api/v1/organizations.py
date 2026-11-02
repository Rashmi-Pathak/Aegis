from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import OrganizationOut

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.get("/current", response_model=OrganizationOut)
def get_current_organization(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve the currently active organization for authenticated user."""
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationOut(
        id=org.id,
        name=org.name,
        slug=org.slug,
        industry=org.industry,
        tier=org.tier,
        healthScore=org.health_score,
        dataQualityScore=org.data_quality_score,
        activeRisksCount=org.active_risks_count,
        createdAt=org.created_at.isoformat() if org.created_at else "",
    )

@router.get("", response_model=List[OrganizationOut])
def list_organizations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List available tenant organizations (admin or current user organizations)."""
    orgs = db.query(Organization).all()
    return [
        OrganizationOut(
            id=o.id,
            name=o.name,
            slug=o.slug,
            industry=o.industry,
            tier=o.tier,
            healthScore=o.health_score,
            dataQualityScore=o.data_quality_score,
            activeRisksCount=o.active_risks_count,
            createdAt=o.created_at.isoformat() if o.created_at else "",
        )
        for o in orgs
    ]
