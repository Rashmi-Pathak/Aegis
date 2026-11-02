from pydantic import BaseModel, Field
from typing import List, Optional

class SchemaField(BaseModel):
    name: str
    type: str
    nullPercentage: float
    hasOutliers: bool

class DatasetItemSchema(BaseModel):
    id: str
    name: str
    sourceType: str
    recordCount: int
    columnCount: int
    qualityScore: float
    lastUpdated: str
    status: str
    schemaFields: Optional[List[SchemaField]] = Field(default=[], alias="schema")

    class Config:
        from_attributes = True
        populate_by_name = True

class ModelIntelligenceItemSchema(BaseModel):
    id: str
    name: str
    type: str
    version: str
    accuracy: str
    mae: str
    rmse: str
    driftStatus: str
    lastTrained: str

    class Config:
        from_attributes = True

class DemoBusinessSchema(BaseModel):
    id: str
    name: str
    industry: str
    tagline: str
    description: str
    zipFileName: str
    datasetCount: int
    recordCount: int
    healthScore: float
    riskCount: int
    primaryRiskStory: dict
    metrics: dict
