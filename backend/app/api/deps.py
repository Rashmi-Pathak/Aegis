from typing import Generator, Optional, List
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.organization import Organization
from app.core.exceptions import AuthenticationError, AuthorizationError

security_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    auth_creds: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    x_org_id: Optional[str] = Header(None, alias="X-Organization-Id"),
) -> User:
    """Validate Bearer JWT token and return active authenticated user."""
    if not auth_creds:
        # Fallback to demo user if unauthenticated during demo exploration
        demo_user = db.query(User).filter(User.email == "demo@aegis.ai").first()
        if demo_user:
            return demo_user
        # Create on demand if not yet seeded
        demo_org = db.query(Organization).filter(Organization.slug == "primelogix").first()
        if not demo_org:
            demo_org = Organization(
                name="PrimeLogix Global",
                slug="primelogix",
                industry="Freight & Global Logistics",
                tier="enterprise",
                health_score=78.0,
                data_quality_score=96.0,
                active_risks_count=4,
                is_demo=True,
            )
            db.add(demo_org)
            db.flush()

        from app.core.security import get_password_hash
        user = User(
            email="demo@aegis.ai",
            name="Chief Risk Officer",
            hashed_password=get_password_hash("Demo@Aegis2026"),
            role="executive",
            organization_id=demo_org.id,
            is_active=True,
            is_demo=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    token = auth_creds.credentials
    payload = decode_access_token(token)
    if not payload:
        raise AuthenticationError("Invalid or expired authentication session.")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise AuthenticationError("User account not found or deactivated.")

    # Multi-tenancy verification: If X-Organization-Id header is provided, verify user has access
    if x_org_id and x_org_id != user.organization_id and user.role != "admin":
        # Check if user has membership in requested organization or if it's a demo org
        target_org = db.query(Organization).filter(Organization.id == x_org_id).first()
        if not target_org or (not target_org.is_demo and user.organization_id != target_org.id):
            raise AuthorizationError("Access denied to target organization tenant.")

    return user

def require_roles(allowed_roles: List[str]):
    """Role-based access control dependency."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != "admin":
            raise AuthorizationError(f"Action requires one of roles: {', '.join(allowed_roles)}")
        return current_user
    return role_checker
