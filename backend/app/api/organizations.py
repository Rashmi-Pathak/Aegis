"""AEGIS Multi-Tenant Organizations Router."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import OrganizationSchema

router = APIRouter(prefix="/organizations", tags=["Multi-Tenancy"])

@router.get("/current", response_model=OrganizationSchema)
def get_current_organization(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns currently authenticated tenant organization."""
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    return org

@router.get("", response_model=List[OrganizationSchema])
def list_organizations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists organizations accessible to administrator."""
    return db.query(Organization).all()
