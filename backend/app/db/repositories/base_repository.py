"""AEGIS Generic SQL Repository Base Pattern
Provides typed CRUD operations, tenant isolation filters, and pagination for SQLAlchemy models.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing standardized tenant-scoped queries."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id: str, organization_id: Optional[str] = None) -> Optional[ModelType]:
        """Fetches single entity by primary key, enforcing tenant scoping if applicable."""
        query = db.query(self.model).filter(self.model.id == id)
        if organization_id and hasattr(self.model, "organization_id"):
            query = query.filter(self.model.organization_id == organization_id)
        return query.first()

    def list_by_tenant(
        self,
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        order_by_col: Optional[str] = None,
        descending: bool = True,
    ) -> List[ModelType]:
        """Lists paginated records strictly isolated to organization_id."""
        query = db.query(self.model)
        if hasattr(self.model, "organization_id"):
            query = query.filter(self.model.organization_id == organization_id)

        if order_by_col and hasattr(self.model, order_by_col):
            col = getattr(self.model, order_by_col)
            query = query.order_by(col.desc() if descending else col.asc())
        elif hasattr(self.model, "created_at"):
            query = query.order_by(self.model.created_at.desc())

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, attributes: Dict[str, Any]) -> ModelType:
        """Instantiates and commits new model record."""
        db_obj = self.model(**attributes)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, updates: Dict[str, Any]) -> ModelType:
        """Updates attributes on existing tracked instance."""
        for field, value in updates.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: str, organization_id: Optional[str] = None) -> bool:
        """Removes instance matching id and tenant scope."""
        obj = self.get_by_id(db, id, organization_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
