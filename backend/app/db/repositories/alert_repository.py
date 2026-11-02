"""AEGIS Alert Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.alert import Alert

class AlertRepository(BaseRepository[Alert]):
    def __init__(self):
        super().__init__(Alert)

    def get_active_unacknowledged(self, db: Session, organization_id: str) -> List[Alert]:
        return (
            db.query(Alert)
            .filter(Alert.organization_id == organization_id, Alert.acknowledged == False)
            .order_by(Alert.severity.desc(), Alert.created_at.desc())
            .all()
        )
