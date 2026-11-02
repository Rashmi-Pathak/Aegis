from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Report(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "reports"

    title = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False) # executive, risk, forecast, data_quality, audit
    frequency = Column(String(32), default="on_demand", nullable=False) # weekly, monthly, on_demand
    status = Column(String(32), default="ready", nullable=False) # generating, ready, failed
    summary = Column(Text, nullable=False)
    content_json = Column(JSON, nullable=True)
    pdf_path = Column(String(512), nullable=True)

    organization = relationship("Organization", back_populates="reports")
