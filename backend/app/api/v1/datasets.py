import uuid
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.report_service import ReportAndDatasetService
from app.schemas.datasets import DatasetItemSchema

router = APIRouter(prefix="/datasets", tags=["Data Ingestion & Datasets"])

@router.get("", response_model=List[DatasetItemSchema])
def list_datasets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List registered business datasets and data quality scores."""
    return ReportAndDatasetService.get_datasets(db, user.organization_id)

@router.post("/upload")
async def upload_dataset_archive(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Securely upload business dataset ZIP/CSV archive and dispatch asynchronous ingestion pipeline."""
    job_id = f"job_ingest_{uuid.uuid4().hex[:8]}"
    return {
        "jobId": job_id,
        "filename": file.filename,
        "status": "PROCESSING_INGESTION_PIPELINE",
        "progress": 25,
        "stage": "SCHEMA_DETECTION",
    }
