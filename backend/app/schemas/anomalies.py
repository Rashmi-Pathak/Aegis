from pydantic import BaseModel
from typing import Optional

class AnomalyItemSchema(BaseModel):
    id: str
    metric: str
    dimension: str
    timestamp: str
    observedValue: float
    expectedValue: float
    deviationPercent: float
    severity: str
    confidence: float
    algorithmUsed: str
    businessImpact: str
    status: str

    class Config:
        from_attributes = True
