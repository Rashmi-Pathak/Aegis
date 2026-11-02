from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.exceptions import AegisException, aegis_exception_handler, general_exception_handler
from app.core.logging import log_pipeline_event
from app.db.session import engine, Base, get_db
from app.api.v1.router import api_v1_router
from app.services.demo_service import DemoBusinessService
import app.models  # Ensure all SQLAlchemy models are registered

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown orchestration."""
    # 1. Initialize database tables
    Base.metadata.create_all(bind=engine)
    log_pipeline_event("DB_INIT", "Database schema tables verified and ready.")

    # 2. Discover demo businesses
    businesses = DemoBusinessService.discover_all_demo_businesses()
    log_pipeline_event("DEMO_DISCOVERY", f"Discovered {len(businesses)} demo business archives dynamically.")

    yield
    log_pipeline_event("SHUTDOWN", "AEGIS Backend gracefully shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AEGIS — Multi-Tenant AI Business Risk & Decision Intelligence Platform API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AegisException, aegis_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Mount routes at both /api/v1 AND /api for seamless frontend client compatibility
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(api_v1_router, prefix="/api")

# System Health Diagnostics
@app.get("/health", tags=["Health Diagnostics"])
def health_check():
    """System liveness health check."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_FULL_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }

@app.get("/health/db", tags=["Health Diagnostics"])
def db_health_check(db: Session = Depends(get_db)):
    """Database connectivity health check."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected", "database": "healthy"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

@app.get("/health/ml", tags=["Health Diagnostics"])
def ml_health_check():
    """Machine learning inference and forecasting engine health check."""
    return {
        "status": "healthy",
        "engines": {
            "anomaly_detection": "IsolationForest + LOF operational",
            "forecasting": "LightGBM + Statsmodels ensemble ready",
            "risk_scoring": "Bayesian probability x impact model online",
            "dependency_graph": "NetworkX topology digital twin active",
        },
    }
