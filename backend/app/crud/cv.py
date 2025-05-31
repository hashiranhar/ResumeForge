from sqlalchemy.orm import Session
from app.models.cv import CV
from typing import List, Optional, Dict, Any
from uuid import UUID

def get_user_cvs(db: Session, user_id: str) -> List[CV]:
    """Get all CVs for a user"""
    return db.query(CV).filter(CV.user_id == user_id).order_by(CV.updated_at.desc()).all()

def get_cv_by_id(db: Session, cv_id: str, user_id: str) -> Optional[CV]:
    """Get a specific CV by ID (only if it belongs to the user)"""
    return db.query(CV).filter(CV.id == cv_id, CV.user_id == user_id).first()

def create_cv(db: Session, user_id: str, name: str, markdown_content: Optional[str] = None, settings: Optional[Dict[str, Any]] = None) -> CV:
    """Create a new CV"""
    db_cv = CV(
        user_id=user_id,
        name=name,
        markdown_content=markdown_content,
        settings=settings or {}
    )
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv

def update_cv(db: Session, cv_id: str, user_id: str, name: Optional[str] = None, markdown_content: Optional[str] = None, settings: Optional[Dict[str, Any]] = None) -> Optional[CV]:
    """Update a CV (only if it belongs to the user)"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == user_id).first()
    if not cv:
        return None
    
    if name is not None:
        cv.name = name
    if markdown_content is not None:
        cv.markdown_content = markdown_content
    if settings is not None:
        cv.settings = settings
    
    db.commit()
    db.refresh(cv)
    return cv

def delete_cv(db: Session, cv_id: str, user_id: str) -> bool:
    """Delete a CV (only if it belongs to the user)"""
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == user_id).first()
    if not cv:
        return False
    
    db.delete(cv)
    db.commit()
    return True