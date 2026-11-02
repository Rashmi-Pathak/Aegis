from sqlalchemy import Column, String, JSON, ForeignKey
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class AuditLog(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "audit_logs"

    user_id = Column(String(64), nullable=True)
    user_email = Column(String(255), nullable=True)
    action = Column(String(128), nullable=False) # LOGIN, DATA_UPLOAD, SIMULATION_RUN, DECISION_APPROVED, etc.
    resource_type = Column(String(64), nullable=False) # risk, forecast, decision, dataset, user
    resource_id = Column(String(64), nullable=True)
    ip_address = Column(String(64), default="127.0.0.1", nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    details_json = Column(JSON, nullable=True)
