from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Dataset(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "datasets"

    name = Column(String(255), nullable=False)
    source_type = Column(String(64), default="zip", nullable=False) # zip, csv, excel, api, postgres
    record_count = Column(Integer, default=0, nullable=False)
    column_count = Column(Integer, default=0, nullable=False)
    quality_score = Column(Float, default=90.0, nullable=False)
    status = Column(String(64), default="ready", nullable=False) # processing, ready, error
    file_path = Column(String(512), nullable=True)
    schema_json = Column(JSON, nullable=True)
    profile_json = Column(JSON, nullable=True)
    quality_metrics_json = Column(JSON, nullable=True)

    organization = relationship("Organization", back_populates="datasets")
