from pydantic import BaseModel, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    organizationId: str
    createdAt: str

    class Config:
        from_attributes = True

class OrganizationOut(BaseModel):
    id: str
    name: str
    slug: str
    industry: str
    tier: str
    healthScore: float
    dataQualityScore: float
    activeRisksCount: int
    createdAt: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = "Demo@Aegis2026"

class SignupRequest(BaseModel):
    name: str
    email: str
    organizationName: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: UserOut
    organization: OrganizationOut
