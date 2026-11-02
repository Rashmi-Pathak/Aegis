from sqlalchemy import Column, String, Float, JSON, ForeignKey
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class MLModel(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "ml_models"

    name = Column(String(255), nullable=False) # e.g. "Multi-Horizon Topline Forecast (LightGBM + ARIMA)"
    type = Column(String(64), nullable=False) # forecasting, anomaly, risk, causal
    version = Column(String(32), default="v1.0.0", nullable=False)
    accuracy = Column(String(32), default="96.5%", nullable=False)
    mae = Column(String(32), default="$0.28M", nullable=False)
    rmse = Column(String(32), default="$0.41M", nullable=False)
    drift_status = Column(String(32), default="stable", nullable=False) # stable, warning, drifting
    status = Column(String(32), default="active", nullable=False)
    last_trained = Column(String(64), nullable=False)
    hyperparameters_json = Column(JSON, nullable=True)
    features_json = Column(JSON, nullable=True)
