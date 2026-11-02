"""AEGIS Canonical Business Data Model
Standardized intermediate domain entities: FinancialRecord, CustomerRecord, ShipmentRecord, InventoryRecord.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CanonicalFinancialRecord(BaseModel):
    transaction_id: str
    date: str
    revenue: float = 0.0
    cogs: float = 0.0
    operating_expenses: float = 0.0
    net_income: float = 0.0
    currency: str = "USD"
    cost_center: Optional[str] = None

class CanonicalCustomerRecord(BaseModel):
    customer_id: str
    company_name: str
    industry: str
    tier: str = "Standard"
    annual_contract_value: float = 0.0
    credit_limit: float = 0.0
    risk_score: float = 0.0

class CanonicalShipmentRecord(BaseModel):
    shipment_id: str
    dispatch_date: str
    origin: str
    destination: str
    distance_miles: float = 0.0
    actual_transit_days: float = 0.0
    is_delayed: bool = False
    freight_cost: float = 0.0
