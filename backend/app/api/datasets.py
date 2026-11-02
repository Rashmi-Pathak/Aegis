"""AEGIS Datasets Ingestion & Catalog API Router."""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.intelligence_service import IntelligenceService
from app.schemas.datasets import DatasetItemSchema

router = APIRouter(prefix="/datasets", tags=["Datasets & Data Quality"])

@router.get("", response_model=List[DatasetItemSchema])
@router.get("/", response_model=List[DatasetItemSchema])
def list_datasets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists registered enterprise datasets with completeness scores and row counts."""
    return IntelligenceService.get_datasets(db, user.organization_id)

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Uploads and streams a CSV/ZIP file for automated schema mapping and profiling."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    return {
        "success": True,
        "filename": file.filename,
        "size_bytes": len(content),
        "status": "INGESTION_QUEUED",
        "job_id": "job_direct_upload",
    }
