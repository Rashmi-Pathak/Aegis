"""AEGIS Anomaly Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.anomaly import Anomaly

class AnomalyRepository(BaseRepository[Anomaly]):
    def __init__(self):
        super().__init__(Anomaly)

    def get_unacknowledged(self, db: Session, organization_id: str) -> List[Anomaly]:
        return (
            db.query(Anomaly)
            .filter(Anomaly.organization_id == organization_id, Anomaly.status != "resolved")
            .order_by(Anomaly.severity.desc(), Anomaly.detected_at.desc())
            .all()
        )
