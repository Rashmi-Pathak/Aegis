from sqlalchemy import Column, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Anomaly(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "anomalies"

    metric = Column(String(255), nullable=False) # e.g. "Fuel Expense Index"
    dimension = Column(String(128), default="overall", nullable=False)
    timestamp = Column(String(64), nullable=False)
    observed_value = Column(Float, nullable=False)
    expected_value = Column(Float, nullable=False)
    deviation_percent = Column(Float, nullable=False)
    severity = Column(String(32), nullable=False) # low, medium, high, critical
    confidence = Column(Float, default=0.92, nullable=False)
    algorithm_used = Column(String(64), default="IsolationForest", nullable=False) # IsolationForest, LOF, ZScore, IQR
    business_impact = Column(String(512), nullable=False)
    status = Column(String(32), default="open", nullable=False) # open, reviewing, resolved

    organization = relationship("Organization", back_populates="anomalies")
