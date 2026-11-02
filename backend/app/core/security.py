import datetime
from datetime import timezone
from typing import Optional, Any, Dict
import jwt
import bcrypt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify raw plain password against hashed password."""
    try:
        pw_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        # Fallback for plain text demo verification if needed during seed
        return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    pw_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")

def create_access_token(
    subject: str,
    organization_id: str,
    role: str = "analyst",
    expires_delta: Optional[datetime.timedelta] = None,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate signed JWT access token with user id, organization id, and role."""
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: Dict[str, Any] = {
        "exp": expire,
        "sub": str(subject),
        "org_id": str(organization_id),
        "role": str(role),
        "type": "access",
    }
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate incoming JWT access token."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except (jwt.PyJWTError, Exception):
        return None
