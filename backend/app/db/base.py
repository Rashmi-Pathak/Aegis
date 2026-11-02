import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class TimestampMixin:
    """Provides created_at and updated_at datetime fields."""
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

class TenantMixin:
    """Enforces strict multi-tenancy scoping via organization_id with foreign key constraint."""
    organization_id = Column(
        String(64),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

class IdMixin:
    """UUID Primary key mixin."""
    id = Column(String(64), primary_key=True, default=generate_uuid, index=True)
