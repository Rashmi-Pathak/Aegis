"""AEGIS Report Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.report import Report

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_recent_reports(self, db: Session, organization_id: str, limit: int = 10) -> List[Report]:
        return (
            db.query(Report)
            .filter(Report.organization_id == organization_id)
            .order_by(Report.created_at.desc())
            .limit(limit)
            .all()
        )
