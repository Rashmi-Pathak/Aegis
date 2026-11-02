from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Risk(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "risks"

    title = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False) # financial, operational, supply_chain, compliance, customer
    severity = Column(String(32), nullable=False) # low, medium, high, critical
    score = Column(Float, nullable=False) # 0 to 100
    probability = Column(Float, nullable=False) # 0.0 to 1.0
    impact = Column(Float, nullable=False) # 0.0 to 100.0
    exposure_amount = Column(String(64), nullable=False) # e.g. "$2.85M" or numeric exposure
    exposure_numeric = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="active", nullable=False) # active, investigating, mitigated, closed
    detected_at = Column(String(64), nullable=False)
    primary_drivers = Column(JSON, nullable=False) # list of strings or driver objects
    secondary_drivers = Column(JSON, nullable=False) # list of strings
    affected_areas = Column(JSON, nullable=False) # list of business areas / KPIs
    recommended_actions = Column(JSON, nullable=False) # list of strings
    evidence_json = Column(JSON, nullable=True) # detailed evidence & signals

    organization = relationship("Organization", back_populates="risks")
