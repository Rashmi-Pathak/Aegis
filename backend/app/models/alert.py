from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Alert(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "alerts"

    severity = Column(String(32), nullable=False) # low, medium, high, critical
    source = Column(String(128), nullable=False) # e.g. "Risk Engine - Energy Module"
    message = Column(String(512), nullable=False)
    affected_metric = Column(String(255), nullable=False)
    action_required = Column(String(512), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    timestamp_str = Column(String(64), nullable=False) # e.g. "12m ago" or ISO

    organization = relationship("Organization", back_populates="alerts")
