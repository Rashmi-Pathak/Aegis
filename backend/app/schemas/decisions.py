from pydantic import BaseModel
from typing import Optional

class DecisionItemSchema(BaseModel):
    id: str
    title: str
    type: str
    recommendation: str
    reasoning: str
    expectedImpact: str
    riskReduction: str
    confidence: float
    status: str
    requiresHumanApproval: bool
    estimatedRoi: str

    class Config:
        from_attributes = True

class DecisionApprovalResponse(BaseModel):
    success: bool
    message: str
