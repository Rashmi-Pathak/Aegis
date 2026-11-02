from pydantic import BaseModel
from typing import List, Optional

class HistoricalPoint(BaseModel):
    date: str
    value: float

class ProjectedPoint(BaseModel):
    date: str
    value: float
    lowerBound: float
    upperBound: float

class AccuracyMetrics(BaseModel):
    mae: float
    rmse: float
    mape: str

class ForecastItemSchema(BaseModel):
    id: str
    metric: str
    horizonDays: int
    modelUsed: str
    confidenceScore: float
    historical: List[HistoricalPoint]
    forecast: List[ProjectedPoint]
    accuracyMetrics: AccuracyMetrics

    class Config:
        from_attributes = True
