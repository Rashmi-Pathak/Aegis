"""AEGIS Comprehensive Repositories, MLOps Champion/Challenger,
and Remaining Industry Vertical Generators.
"""

import os

FILES = {
    "backend/app/db/repositories/user_repository.py": '''"""AEGIS User Database Repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def list_by_role(self, db: Session, organization_id: str, role: str) -> List[User]:
        return db.query(User).filter(User.organization_id == organization_id, User.role == role).all()
''',
    "backend/app/db/repositories/organization_repository.py": '''"""AEGIS Organization Database Repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.organization import Organization

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self):
        super().__init__(Organization)

    def get_by_slug(self, db: Session, slug: str) -> Optional[Organization]:
        return db.query(Organization).filter(Organization.slug == slug).first()

    def update_health_score(self, db: Session, organization_id: str, new_score: float) -> Optional[Organization]:
        org = self.get_by_id(db, organization_id)
        if org:
            org.health_score = new_score
            db.commit()
            db.refresh(org)
        return org
''',
    "backend/app/db/repositories/dataset_repository.py": '''"""AEGIS Dataset Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.dataset import Dataset

class DatasetRepository(BaseRepository[Dataset]):
    def __init__(self):
        super().__init__(Dataset)

    def list_ready_datasets(self, db: Session, organization_id: str) -> List[Dataset]:
        return db.query(Dataset).filter(Dataset.organization_id == organization_id, Dataset.status == "ready").all()
''',
    "backend/app/db/repositories/forecast_repository.py": '''"""AEGIS Forecast Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.forecast import Forecast

class ForecastRepository(BaseRepository[Forecast]):
    def __init__(self):
        super().__init__(Forecast)

    def get_latest_metric_forecast(self, db: Session, organization_id: str, metric: str) -> Optional[Forecast]:
        return (
            db.query(Forecast)
            .filter(Forecast.organization_id == organization_id, Forecast.metric == metric)
            .order_by(Forecast.created_at.desc())
            .first()
        )
''',
    "backend/app/db/repositories/decision_repository.py": '''"""AEGIS Decision Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.decision import Decision

class DecisionRepository(BaseRepository[Decision]):
    def __init__(self):
        super().__init__(Decision)

    def get_pending_approvals(self, db: Session, organization_id: str) -> List[Decision]:
        return (
            db.query(Decision)
            .filter(Decision.organization_id == organization_id, Decision.status == "pending_review")
            .all()
        )
''',
    "backend/app/db/repositories/report_repository.py": '''"""AEGIS Report Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.report import Report

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_recent_reports(self, db: Session, organization_id: str, limit: int = 10) -> List[Report]:
        return (
            db.query(Report)
            .filter(Report.organization_id == organization_id)
            .order_by(Report.created_at.desc())
            .limit(limit)
            .all()
        )
''',
    "backend/app/db/repositories/alert_repository.py": '''"""AEGIS Alert Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.alert import Alert

class AlertRepository(BaseRepository[Alert]):
    def __init__(self):
        super().__init__(Alert)

    def get_active_unacknowledged(self, db: Session, organization_id: str) -> List[Alert]:
        return (
            db.query(Alert)
            .filter(Alert.organization_id == organization_id, Alert.acknowledged == False)
            .order_by(Alert.severity.desc(), Alert.created_at.desc())
            .all()
        )
''',
    "backend/app/db/repositories/audit_repository.py": '''"""AEGIS Audit Log Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.audit_log import AuditLog

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    def get_organization_audit_trail(self, db: Session, organization_id: str, limit: int = 100) -> List[AuditLog]:
        return (
            db.query(AuditLog)
            .filter(AuditLog.organization_id == organization_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
''',
    "backend/app/mlops/champion_challenger.py": '''"""AEGIS MLOps Champion/Challenger Model Shadow Router
Routes incoming telemetry to both Champion (active) and Challenger (shadow) models
to benchmark inference accuracy and detect degradation before promotion.
"""
from typing import Dict, Any, List, Optional
import numpy as np

class ChampionChallengerRouter:
    @staticmethod
    def compare_inference(
        champion_model_id: str,
        challenger_model_id: str,
        ground_truth: float,
        champion_prediction: float,
        challenger_prediction: float,
    ) -> Dict[str, Any]:
        """Compares prediction error on actual outcome."""
        champ_err = abs(ground_truth - champion_prediction)
        chall_err = abs(ground_truth - challenger_prediction)

        challenger_outperformed = bool(chall_err < champ_err)
        margin_improvement_pct = ((champ_err - chall_err) / (champ_err or 1.0)) * 100.0

        return {
            "champion_id": champion_model_id,
            "challenger_id": challenger_model_id,
            "ground_truth": ground_truth,
            "champion_error": round(champ_err, 3),
            "challenger_error": round(chall_err, 3),
            "challenger_outperformed": challenger_outperformed,
            "error_reduction_pct": round(margin_improvement_pct, 2),
            "promotion_recommendation": "PROMOTE_CHALLENGER" if (challenger_outperformed and margin_improvement_pct > 15.0) else "RETAIN_CHAMPION",
        }
''',
    "backend/app/synthetic/automotive_oem_generator.py": '''"""AEGIS Automotive Tier-1 Supply & Assembly Telemetry Generator
Generates component serial lots, torque sensor telemetry, weld inspections, and warranty claim hazards.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class AutomotiveOEMGenerator:
    COMPONENTS = ["Steering Column Assembly", "Brake Caliper Module", "Transmission Housing", "Battery Thermal Pack"]

    @classmethod
    def generate_automotive_ecosystem(
        cls,
        n_lots: int = 250,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        lots = []
        for l in range(1, n_lots + 1):
            comp = random.choice(cls.COMPONENTS)
            lot_size = random.randint(500, 5000)
            torque_nm = float(np.random.normal(85.0, 3.5))
            weld_failures = int(np.random.poisson(2.5))
            warranty_claims_rate = float(np.random.beta(1.5, 400.0) * 100.0)

            lots.append({
                "lot_id": f"LOT-{l:05d}",
                "component_name": comp,
                "lot_size_units": lot_size,
                "average_torque_nm": round(torque_nm, 2),
                "weld_defect_count": weld_failures,
                "warranty_claims_per_1000": round(warranty_claims_rate, 2),
                "recall_risk_flag": bool(weld_failures > 8 or torque_nm < 75.0),
            })

        return pd.DataFrame(lots)
''',
    "backend/app/synthetic/food_cold_chain_generator.py": '''"""AEGIS Agriculture & Perishable Food Processing Generator
Generates harvest lot yields, cold storage temperature telemetry, and shelf-life decay curves.
"""
from typing import Dict, Any, List
import random
import numpy as np
import pandas as pd

class FoodColdChainGenerator:
    COMMODITIES = ["Organic Strawberries", "Dairy Creamery", "Frozen Poultry", "Fresh Atlantic Salmon"]

    @classmethod
    def generate_cold_chain_logs(
        cls,
        n_shipments: int = 300,
        seed: int = 42,
    ) -> pd.DataFrame:
        np.random.seed(seed)
        random.seed(seed)

        records = []
        for i in range(1, n_shipments + 1):
            item = random.choice(cls.COMMODITIES)
            target_temp = 2.0 if "Frozen" not in item else -18.0
            actual_temp = target_temp + float(np.random.normal(0.0, 1.2))
            hours_in_transit = random.randint(12, 96)
            breach = bool(actual_temp > (target_temp + 3.0))

            spoilage_cost = round(random.randint(5000, 35000) * 0.40, 2) if breach else 0.0

            records.append({
                "consignment_id": f"FD-{i:05d}",
                "commodity": item,
                "target_temp_celsius": target_temp,
                "mean_actual_temp_celsius": round(actual_temp, 1),
                "transit_hours": hours_in_transit,
                "temperature_excursion_breach": breach,
                "spoilage_loss_usd": spoilage_cost,
            })

        return pd.DataFrame(records)
''',
    "backend/tests/test_all_repositories.py": '''"""AEGIS Full Database Repositories Test Suite."""
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
''',
    "backend/tests/test_champion_challenger.py": '''"""AEGIS MLOps Champion/Challenger Test Suite."""
import pytest
from app.mlops.champion_challenger import ChampionChallengerRouter

def test_champion_challenger_comparison():
    res = ChampionChallengerRouter.compare_inference(
        champion_model_id="iso_forest_v1",
        challenger_model_id="iso_forest_v2",
        ground_truth=100.0,
        champion_prediction=112.0,  # Error 12
        challenger_prediction=103.0, # Error 3 (much better)
    )
    assert res["challenger_outperformed"] is True
    assert res["promotion_recommendation"] == "PROMOTE_CHALLENGER"
    assert res["error_reduction_pct"] > 50.0
'''
}

for path, code in FILES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Wrote {path}")

print("Repositories and MLOps modules generated successfully.")
