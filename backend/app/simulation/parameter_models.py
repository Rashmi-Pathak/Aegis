"""AEGIS Simulation Shock Parameter Domain Models
Defines typed bounded parameter models for What-If scenario simulations.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class FuelShockParameters(BaseModel):
    fuel_price_hike_pct: float = Field(default=20.0, ge=-50.0, le=200.0)
    route_efficiency_adjustment: float = Field(default=0.0, ge=-20.0, le=50.0)

class PortCongestionParameters(BaseModel):
    dwell_days_delta: float = Field(default=3.5, ge=0.0, le=30.0)
    demurrage_cost_per_day: float = Field(default=350.0, ge=50.0, le=5000.0)
