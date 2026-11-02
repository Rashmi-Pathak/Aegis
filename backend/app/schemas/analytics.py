from pydantic import BaseModel
from typing import List, Optional

class MetricSummary(BaseModel):
    title: str
    value: str
    changePercent: float
    trend: str # "up" | "down" | "neutral"
    timeframe: str
    isAnomaly: Optional[bool] = False

class RevenueTrendPoint(BaseModel):
    date: str
    actual: float
    target: float

class MarginBreakdown(BaseModel):
    category: str
    value: float

class CategoryPerformance(BaseModel):
    name: str
    revenue: float
    margin: float
    riskScore: float

class AnalyticsOverview(BaseModel):
    healthScore: float
    kpis: dict
    revenueTrend: List[RevenueTrendPoint]
    marginBreakdown: List[MarginBreakdown]
    categoryPerformance: List[CategoryPerformance]
