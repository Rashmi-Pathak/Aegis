from pydantic import BaseModel
from typing import Optional

class ReportItemSchema(BaseModel):
    id: str
    title: str
    category: str
    generatedAt: str
    frequency: str
    status: str
    summary: str

    class Config:
        from_attributes = True

class AlertItemSchema(BaseModel):
    id: str
    timestamp: str
    severity: str
    source: str
    message: str
    affectedMetric: str
    actionRequired: str
    isRead: bool

    class Config:
        from_attributes = True
