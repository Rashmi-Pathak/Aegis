from sqlalchemy import Column, String, Integer, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin

class Organization(Base, IdMixin, TimestampMixin):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    industry = Column(String(255), nullable=False)
    country = Column(String(128), default="India", nullable=False)
    currency = Column(String(32), default="INR", nullable=False)
    tier = Column(String(64), default="enterprise", nullable=False) # starter, growth, enterprise
    health_score = Column(Float, default=78.0, nullable=False)
    data_quality_score = Column(Float, default=95.0, nullable=False)
    active_risks_count = Column(Integer, default=0, nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False)
    demo_zip_filename = Column(String(255), nullable=True)
    metadata_json = Column(JSON, nullable=True)

    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    datasets = relationship("Dataset", back_populates="organization", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="organization", cascade="all, delete-orphan")
    anomalies = relationship("Anomaly", back_populates="organization", cascade="all, delete-orphan")
    forecasts = relationship("Forecast", back_populates="organization", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="organization", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="organization", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="organization", cascade="all, delete-orphan")
    jobs = relationship("DataJob", back_populates="organization", cascade="all, delete-orphan")
