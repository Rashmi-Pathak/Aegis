from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class BusinessGraph(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "business_graphs"

    name = Column(String(255), default="Enterprise Business Digital Twin", nullable=False)
    nodes_json = Column(JSON, nullable=False) # list of { id, label, category, status, value, riskScore, dependencies }
    edges_json = Column(JSON, nullable=False) # list of { source, target, weight, relationship, isStressed }
    topology_metadata = Column(JSON, nullable=True) # graph density, cycle count, critical path
