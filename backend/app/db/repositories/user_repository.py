"""AEGIS User Database Repository."""
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
