from pydantic import BaseModel
from typing import List, Optional

class SimulationParams(BaseModel):
    priceDelta: float = 0.0
    marketingSpendDelta: float = 0.0
    inventoryBufferDelta: float = 0.0
    procurementDelta: float = 0.0
    hiringDelta: Optional[int] = 0

class SimulationResult(BaseModel):
    baselineRevenue: float
    simulatedRevenue: float
    baselineProfit: float
    simulatedProfit: float
    baselineCashFlow: float
    simulatedCashFlow: float
    baselineRiskScore: int
    simulatedRiskScore: int
    tradeoffs: List[str]
