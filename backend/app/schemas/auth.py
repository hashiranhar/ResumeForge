from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool = False
    
    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Email verification schemas
class EmailVerificationRequest(BaseModel):
    email: EmailStr
    verification_code: str

class ResendVerificationRequest(BaseModel):
    email: EmailStr

class VerificationResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None