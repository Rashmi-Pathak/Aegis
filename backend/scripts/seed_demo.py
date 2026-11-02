import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal, Base, engine
from app.models.organization import Organization
from app.models.user import User
from app.models.risk import Risk
from app.models.anomaly import Anomaly
from app.models.forecast import Forecast
from app.models.decision import Decision
from app.models.report import Report
from app.models.alert import Alert
from app.core.security import get_password_hash
from app.services.demo_service import DemoBusinessService
from app.engines.risk.risk_engine import RiskIntelligenceEngine
from app.engines.anomaly.anomaly_engine import AnomalyDetectionEngine
from app.engines.forecasting.forecast_engine import ForecastingEngine
from app.engines.decision.decision_engine import DecisionIntelligenceEngine
from app.services.report_service import ReportAndDatasetService

def seed_database():
    """Initializes tables, seeds demo user/org, and registers discovered business twins."""
    print("Initializing AEGIS database schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Discover all demo businesses from data/demo-businesses/
        businesses = DemoBusinessService.discover_all_demo_businesses()
        print(f"Dynamically discovered {len(businesses)} demo business ZIP archives.")

        # 2. Seed or update PrimeLogix demo organization
        org = db.query(Organization).filter(Organization.slug == "primelogix").first()
        if not org:
            org = Organization(
                name="PrimeLogix Global",
                slug="primelogix",
                industry="Freight & Global Logistics",
                country="India",
                currency="INR",
                tier="enterprise",
                health_score=78.0,
                data_quality_score=96.0,
                active_risks_count=4,
                is_demo=True,
                demo_zip_filename="PrimeLogix_Aegis_Demo.zip",
            )
            db.add(org)
            db.flush()
            print("Created default PrimeLogix organization.")
        else:
            print("PrimeLogix organization already exists.")

        # 3. Seed official demo user
        demo_user = db.query(User).filter(User.email == "demo@aegis.ai").first()
        if not demo_user:
            demo_user = User(
                email="demo@aegis.ai",
                name="Chief Risk Officer",
                hashed_password=get_password_hash("Demo@Aegis2026"),
                role="executive",
                organization_id=org.id,
                is_active=True,
                is_demo=True,
            )
            db.add(demo_user)
            print("Created demo user: demo@aegis.ai / Demo@Aegis2026")
        else:
            print("Demo user demo@aegis.ai already exists.")

        # 4. Seed other discovered organizations if not present
        for b in businesses:
            if b["id"] != "primelogix":
                existing_org = db.query(Organization).filter(Organization.slug == b["id"]).first()
                if not existing_org:
                    new_org = Organization(
                        name=b["name"],
                        slug=b["id"],
                        industry=b["industry"],
                        tier="enterprise",
                        health_score=float(b["healthScore"]),
                        data_quality_score=94.0,
                        active_risks_count=int(b["riskCount"]),
                        is_demo=True,
                        demo_zip_filename=b["zipFileName"],
                    )
                    db.add(new_org)

        db.commit()
        print("AEGIS database successfully seeded and ready!")

    except Exception as e:
        db.rollback()
        print(f"Seeding error: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
