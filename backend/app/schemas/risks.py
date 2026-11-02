from pydantic import BaseModel
from typing import List, Optional

class RiskItemSchema(BaseModel):
    id: str
    title: str
    category: str
    severity: str
    score: float
    probability: float
    impact: float
    exposureAmount: str
    detectedAt: str
    status: str
    primaryDrivers: List[str]
    secondaryDrivers: List[str]
    affectedAreas: List[str]
    recommendedActions: List[str]

    class Config:
        from_attributes = True

class RiskInvestigationSchema(BaseModel):
    risk: RiskItemSchema
    evidence: List[dict]
    causalChain: List[str]
    forecastImpact: dict
    recommendedActions: List[str]
