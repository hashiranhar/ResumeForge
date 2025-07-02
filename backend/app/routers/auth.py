from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.crud.user import create_user, authenticate_user, get_user_by_email, get_user_by_id, update_last_login
from app.core.security import create_access_token, verify_token, get_password_hash, get_current_user
from app.core.config import settings
from app.services.email import send_reset_email

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = create_user(db, user_data.email, user_data.password)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token"""
    # Authenticate user (OAuth2 uses 'username' field for email)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    update_last_login(db, user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, request.email)
    if not user:
        return {"message": "If your email is registered, a reset link has been sent."}

    # Generate a reset token (JWT with short expiry)
    token = create_access_token(
        subject=str(user.id),
        expires_delta=settings.password_reset_token_expire_minutes
    )

    reset_link = f"http://localhost:5173/auth/reset-password?token={token}"

    # Send email in background
    background_tasks.add_task(
        send_reset_email, user.email, reset_link
    )

    return {"message": "If your email is registered, a reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user_id = verify_token(request.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    return {"message": "Password reset successful"}