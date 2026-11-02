"""AEGIS Forecast Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.forecast import Forecast

class ForecastRepository(BaseRepository[Forecast]):
    def __init__(self):
        super().__init__(Forecast)

    def get_latest_metric_forecast(self, db: Session, organization_id: str, metric: str) -> Optional[Forecast]:
        return (
            db.query(Forecast)
            .filter(Forecast.organization_id == organization_id, Forecast.metric == metric)
            .order_by(Forecast.created_at.desc())
            .first()
        )
