from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Decision(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "decisions"

    title = Column(String(255), nullable=False)
    type = Column(String(64), nullable=False) # operations, pricing, budget, supply_chain, inventory
    recommendation = Column(String(1024), nullable=False)
    reasoning = Column(String(1024), nullable=False)
    expected_impact = Column(String(512), nullable=False)
    risk_reduction = Column(String(512), nullable=False)
    confidence = Column(Float, default=0.9, nullable=False)
    status = Column(String(32), default="pending", nullable=False) # pending, under_review, approved, rejected, executed
    requires_human_approval = Column(Boolean, default=True, nullable=False)
    estimated_roi = Column(String(128), default="3.5x", nullable=False)
    evidence_json = Column(JSON, nullable=True)

    organization = relationship("Organization", back_populates="decisions")
