from pydantic import BaseModel
from typing import List, Optional

class BusinessGraphNode(BaseModel):
    id: str
    label: str
    category: str
    status: str
    value: str
    riskScore: float
    dependencies: List[str]

class BusinessGraphEdge(BaseModel):
    source: str
    target: str
    weight: float
    relationship: str
    isStressed: Optional[bool] = False

class BusinessGraphData(BaseModel):
    nodes: List[BusinessGraphNode]
    edges: List[BusinessGraphEdge]
