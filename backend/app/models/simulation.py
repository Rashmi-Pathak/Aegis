from sqlalchemy import Column, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base import IdMixin, TimestampMixin, TenantMixin

class Simulation(Base, IdMixin, TimestampMixin, TenantMixin):
    __tablename__ = "simulations"

    title = Column(String(255), default="Counterfactual Scenario Run", nullable=False)
    input_params = Column(JSON, nullable=False) # priceDelta, marketingSpendDelta, inventoryBufferDelta, procurementDelta, etc.
    baseline_metrics = Column(JSON, nullable=False)
    simulated_metrics = Column(JSON, nullable=False)
    tradeoffs = Column(JSON, nullable=False) # list of trade-off observations
