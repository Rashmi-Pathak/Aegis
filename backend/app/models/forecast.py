from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Forecast(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "forecasts"

    metric = Column(String(255), nullable=False) # e.g. "Gross Operating Revenue Forecast"
    horizon_days = Column(Integer, default=90, nullable=False)
    model_used = Column(String(128), default="Ensemble (LightGBM + Statsmodels)", nullable=False)
    confidence_score = Column(Float, default=0.94, nullable=False)
    historical_series = Column(JSON, nullable=False) # list of { date: str, value: float }
    forecast_series = Column(JSON, nullable=False) # list of { date: str, value: float, lowerBound: float, upperBound: float }
    accuracy_metrics = Column(JSON, nullable=False) # { mae: float, rmse: float, mape: str }

    organization = relationship("Organization", back_populates="forecasts")
