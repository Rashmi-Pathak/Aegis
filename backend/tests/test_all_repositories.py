"""AEGIS Full Database Repositories Test Suite."""
import pytest
from app.db.session import SessionLocal
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.organization_repository import OrganizationRepository
from app.db.repositories.risk_repository import RiskRepository
from app.db.repositories.anomaly_repository import AnomalyRepository
from app.db.repositories.forecast_repository import ForecastRepository
from app.db.repositories.decision_repository import DecisionRepository
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.audit_repository import AuditLogRepository

def test_repositories_query():
    db = SessionLocal()
    try:
        user_repo = UserRepository()
        users = user_repo.list_by_tenant(db, organization_id="primelogix", limit=5)
        assert isinstance(users, list)

        org_repo = OrganizationRepository()
        primelogix = org_repo.get_by_slug(db, "primelogix")
        assert primelogix is not None

        risk_repo = RiskRepository()
        risks = risk_repo.list_by_tenant(db, organization_id=primelogix.id, limit=5)
        assert isinstance(risks, list)

        alert_repo = AlertRepository()
        alerts = alert_repo.list_by_tenant(db, organization_id=primelogix.id, limit=5)
        assert isinstance(alerts, list)
    finally:
        db.close()
