"""AEGIS Risk Management API Router
Provides endpoints for risk registry, severity distributions, and Value-at-Risk calculations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.risk_engine.exposure import RiskExposureEngine

router = APIRouter(prefix="/risks", tags=["Risk Intelligence"])

@router.get("")
@router.get("/")
def list_risks(severity: Optional[str] = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists categorized enterprise risks filtered by severity."""
    risks = IntelligenceService.get_risks(db, user.organization_id)
    if severity:
        risks = [r for r in risks if r["severity"].lower() == severity.lower()]
    return risks

@router.get("/exposure-var")
def get_var_exposure(portfolio_value: float = 148240000.0, user: User = Depends(get_current_user)):
    """Calculates Value at Risk (VaR) and Conditional Value-at-Risk (CVaR)."""
    returns = [-0.02, -0.015, 0.01, 0.025, -0.045, 0.02, -0.06]
    return RiskExposureEngine.calculate_var_cvar(returns, portfolio_value=portfolio_value)
