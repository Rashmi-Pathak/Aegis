"""AEGIS User Management Router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.auth import UserSchema

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserSchema)
def get_me(user: User = Depends(get_current_user)):
    """Returns profile for currently authenticated user."""
    return user
