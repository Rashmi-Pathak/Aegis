"""AEGIS Organization Database Repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.organization import Organization

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self):
        super().__init__(Organization)

    def get_by_slug(self, db: Session, slug: str) -> Optional[Organization]:
        return db.query(Organization).filter(Organization.slug == slug).first()

    def update_health_score(self, db: Session, organization_id: str, new_score: float) -> Optional[Organization]:
        org = self.get_by_id(db, organization_id)
        if org:
            org.health_score = new_score
            db.commit()
            db.refresh(org)
        return org
