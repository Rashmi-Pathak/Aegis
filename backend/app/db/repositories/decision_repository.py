"""AEGIS Decision Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.decision import Decision

class DecisionRepository(BaseRepository[Decision]):
    def __init__(self):
        super().__init__(Decision)

    def get_pending_approvals(self, db: Session, organization_id: str) -> List[Decision]:
        return (
            db.query(Decision)
            .filter(Decision.organization_id == organization_id, Decision.status == "pending_review")
            .all()
        )
