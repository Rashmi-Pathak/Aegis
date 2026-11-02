from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.demo import router as demo_router
from app.api.v1.organizations import router as org_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.risks import router as risks_router
from app.api.v1.anomalies import router as anomalies_router
from app.api.v1.forecasts import router as forecasts_router
from app.api.v1.decisions import router as decisions_router
from app.api.v1.simulation import router as simulation_router
from app.api.v1.graph import router as graph_router
from app.api.v1.reports import router as reports_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.datasets import router as datasets_router
from app.api.v1.models import router as models_router
from app.api.v1.admin import router as admin_router
from app.api.v1.ws import router as ws_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(demo_router)
api_v1_router.include_router(org_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(risks_router)
api_v1_router.include_router(anomalies_router)
api_v1_router.include_router(forecasts_router)
api_v1_router.include_router(decisions_router)
api_v1_router.include_router(simulation_router)
api_v1_router.include_router(graph_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(datasets_router)
api_v1_router.include_router(models_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(ws_router)
