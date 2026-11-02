from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class DataJob(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "data_jobs"

    job_type = Column(String(64), nullable=False) # ingestion, profiling, analytics, anomaly, forecast, risk, simulation, report
    status = Column(String(64), default="queued", nullable=False) # queued, processing, completed, failed
    progress = Column(Integer, default=0, nullable=False) # 0 to 100
    stage = Column(String(128), default="INITIALIZING", nullable=False)
    error_message = Column(String(1024), nullable=True)
    result_json = Column(JSON, nullable=True)
    metadata_json = Column(JSON, nullable=True)

    organization = relationship("Organization", back_populates="jobs")
