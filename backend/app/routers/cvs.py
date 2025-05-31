from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cv import CVCreate, CVUpdate, CVResponse, CVListResponse
from app.schemas.auth import UserResponse
from app.crud.cv import get_user_cvs, get_cv_by_id, create_cv, update_cv, delete_cv
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/cvs", tags=["cvs"])

@router.get("/", response_model=List[CVListResponse])
def get_cvs(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all CVs for the current user"""
    cvs = get_user_cvs(db, str(current_user.id))
    return cvs

@router.get("/{cv_id}", response_model=CVResponse)
def get_cv(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific CV by ID"""
    cv = get_cv_by_id(db, cv_id, str(current_user.id))
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    return cv

@router.post("/", response_model=CVResponse)
def create_new_cv(
    cv_data: CVCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new CV"""
    cv = create_cv(
        db=db,
        user_id=str(current_user.id),
        name=cv_data.name,
        markdown_content=cv_data.markdown_content,
        settings=cv_data.settings
    )
    return cv

@router.put("/{cv_id}", response_model=CVResponse)
def update_cv_endpoint(
    cv_id: str,
    cv_data: CVUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing CV"""
    cv = update_cv(
        db=db,
        cv_id=cv_id,
        user_id=str(current_user.id),
        name=cv_data.name,
        markdown_content=cv_data.markdown_content,
        settings=cv_data.settings
    )
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    return cv

@router.delete("/{cv_id}")
def delete_cv_endpoint(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a CV"""
    success = delete_cv(db, cv_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    return {"message": "CV deleted successfully"}