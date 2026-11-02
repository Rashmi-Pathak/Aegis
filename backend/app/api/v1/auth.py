from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import LoginRequest, SignupRequest, AuthResponse, UserOut
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=AuthResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with credentials and return JWT token and organization info."""
    return AuthService.authenticate_user(db, credentials)

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    """Provision a new enterprise tenant organization and executive user."""
    return AuthService.register_user(db, req)

@router.get("/me", response_model=UserOut)
def get_current_user_profile(user: User = Depends(get_current_user)):
    """Retrieve current authenticated user session."""
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        organizationId=user.organization_id,
        createdAt=user.created_at.isoformat() if user.created_at else "",
    )
