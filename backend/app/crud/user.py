from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from datetime import datetime

def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password: str) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def update_last_login(db: Session, user: User) -> User:
    """Update user's last login timestamp"""
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user