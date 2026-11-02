"""AEGIS Risk and Anomaly Database Repositories
Specialized queries for threat categorization, status transitions, and severity filtering.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.risk import Risk
from app.models.anomaly import Anomaly


class RiskRepository(BaseRepository[Risk]):
    """Query interface for persistent enterprise business risks."""

    def __init__(self):
        super().__init__(Risk)

    def get_critical_risks(self, db: Session, organization_id: str) -> List[Risk]:
        """Returns risks with severity == 'critical' or score >= 75."""
        return (
            db.query(Risk)
            .filter(Risk.organization_id == organization_id)
            .filter((Risk.severity == "critical") | (Risk.score >= 75.0))
            .order_by(Risk.score.desc())
            .all()
        )

    def get_by_category(self, db: Session, organization_id: str, category: str) -> List[Risk]:
        """Filters risks by operational or financial category."""
        return (
            db.query(Risk)
            .filter(Risk.organization_id == organization_id, Risk.category == category)
            .order_by(Risk.score.desc())
            .all()
        )


class AnomalyRepository(BaseRepository[Anomaly]):
    """Query interface for telemetry and time-series anomalies."""

    def __init__(self):
        super().__init__(Anomaly)

    def get_unacknowledged(self, db: Session, organization_id: str) -> List[Anomaly]:
        """Returns anomalies requiring operational review."""
        return (
            db.query(Anomaly)
            .filter(Anomaly.organization_id == organization_id, Anomaly.status != "resolved")
            .order_by(Anomaly.severity.desc(), Anomaly.detected_at.desc())
            .all()
        )
