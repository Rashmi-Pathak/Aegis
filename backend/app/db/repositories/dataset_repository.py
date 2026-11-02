"""AEGIS Dataset Database Repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.repositories.base_repository import BaseRepository
from app.models.dataset import Dataset

class DatasetRepository(BaseRepository[Dataset]):
    def __init__(self):
        super().__init__(Dataset)

    def list_ready_datasets(self, db: Session, organization_id: str) -> List[Dataset]:
        return db.query(Dataset).filter(Dataset.organization_id == organization_id, Dataset.status == "ready").all()
