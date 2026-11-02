import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.organization import Organization
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import AuthenticationError, NotFoundError
from app.schemas.auth import LoginRequest, SignupRequest, AuthResponse, UserOut, OrganizationOut

class AuthService:
    """Manages user authentication, tenant registration, and JWT sessions."""

    @classmethod
    def authenticate_user(cls, db: Session, credentials: LoginRequest) -> AuthResponse:
        """Authenticate user against database records or seeded demo user."""
        email = credentials.email.strip().lower()
        
        # Check database for existing user
        user = db.query(User).filter(User.email == email).first()

        # If user not found, check if it's the official demo user
        if not user and (email in ["demo@aegis.ai", "executive@aegis.ai", "executive@primelogix.com"]):
            # Create/ensure demo org and user
            org = db.query(Organization).filter(Organization.slug == "primelogix").first()
            if not org:
                org = Organization(
                    name="PrimeLogix Global",
                    slug="primelogix",
                    industry="Freight & Global Logistics",
                    tier="enterprise",
                    health_score=78.0,
                    data_quality_score=96.0,
                    active_risks_count=4,
                    is_demo=True,
                )
                db.add(org)
                db.flush()

            user = User(
                email=email,
                name="Chief Risk Officer",
                hashed_password=get_password_hash("Demo@Aegis2026"),
                role="executive",
                organization_id=org.id,
                is_active=True,
                is_demo=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        if not user:
            raise AuthenticationError("User not found or invalid credentials")

        # Verify password if provided
        if credentials.password:
            if not verify_password(credentials.password, user.hashed_password):
                # Allow standard demo password for demo users
                if not (user.is_demo and credentials.password == "Demo@Aegis2026"):
                    raise AuthenticationError("Invalid password")

        org = db.query(Organization).filter(Organization.id == user.organization_id).first()
        if not org:
            raise NotFoundError("Associated organization not found")

        # Issue JWT
        token = create_access_token(subject=user.id, organization_id=org.id, role=user.role)

        user_out = UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            organizationId=user.organization_id,
            createdAt=user.created_at.isoformat() if user.created_at else datetime.datetime.utcnow().isoformat(),
        )

        org_out = OrganizationOut(
            id=org.id,
            name=org.name,
            slug=org.slug,
            industry=org.industry,
            tier=org.tier,
            healthScore=org.health_score,
            dataQualityScore=org.data_quality_score,
            activeRisksCount=org.active_risks_count,
            createdAt=org.created_at.isoformat() if org.created_at else datetime.datetime.utcnow().isoformat(),
        )

        return AuthResponse(token=token, user=user_out, organization=org_out)

    @classmethod
    def register_user(cls, db: Session, req: SignupRequest) -> AuthResponse:
        """Register a new enterprise tenant and initial administrative user."""
        email = req.email.strip().lower()
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            # Login if user already exists
            return cls.authenticate_user(db, LoginRequest(email=email, password=req.password))

        slug = req.organizationName.lower().replace(" ", "_")
        org = Organization(
            name=req.organizationName,
            slug=slug,
            industry="Enterprise Commerce",
            tier="growth",
            health_score=82.0,
            data_quality_score=94.0,
            active_risks_count=0,
            is_demo=False,
        )
        db.add(org)
        db.flush()

        user = User(
            email=email,
            name=req.name,
            hashed_password=get_password_hash(req.password),
            role="executive",
            organization_id=org.id,
            is_active=True,
            is_demo=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(subject=user.id, organization_id=org.id, role=user.role)

        user_out = UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            organizationId=user.organization_id,
            createdAt=user.created_at.isoformat(),
        )

        org_out = OrganizationOut(
            id=org.id,
            name=org.name,
            slug=org.slug,
            industry=org.industry,
            tier=org.tier,
            healthScore=org.health_score,
            dataQualityScore=org.data_quality_score,
            activeRisksCount=org.active_risks_count,
            createdAt=org.created_at.isoformat(),
        )

        return AuthResponse(token=token, user=user_out, organization=org_out)
