from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.template import TemplateResponse, CreateCVFromTemplate
from app.schemas.cv import CVResponse
from app.schemas.auth import UserResponse
from app.crud.template import get_all_templates, get_template_by_id
from app.crud.cv import create_cv
from app.routers.auth import get_current_user
from app.services.rate_limiting_service import check_cv_creation_rate_limit

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.get("/", response_model=List[TemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    """Get all available templates"""
    templates = get_all_templates(db)
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific template by ID"""
    template = get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template

@router.post("/create-cv", response_model=CVResponse)
def create_cv_from_template(
    template_data: CreateCVFromTemplate,
    cv_limit_check = Depends(check_cv_creation_rate_limit()),  # CV creation rate limiting added
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new CV from a template"""
    # Get the template
    template = get_template_by_id(db, str(template_data.template_id))
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Create CV with template content
    cv = create_cv(
        db=db,
        user_id=str(current_user.id),
        name=template_data.cv_name,
        markdown_content=template.markdown_content,
        settings=template.settings
    )
    return cv

