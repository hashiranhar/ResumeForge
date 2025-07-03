from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cv import CVCreate, CVUpdate, CVResponse, CVListResponse
from app.schemas.auth import UserResponse
from app.crud.cv import get_user_cvs, get_cv_by_id, create_cv, update_cv, delete_cv
from app.routers.auth import get_current_user
from app.services.pdf_service import pdf_service
from app.services.rate_limiting_service import check_cv_creation_rate_limit
import logging

logger = logging.getLogger(__name__)
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
    cv_limit_check = Depends(check_cv_creation_rate_limit()),  # CV creation rate limiting added
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

@router.get("/{cv_id}/pdf")
def download_cv_pdf(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate and download CV as PDF"""
    # Get the CV
    cv = get_cv_by_id(db, cv_id, str(current_user.id))
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    try:
        # Generate PDF
        pdf_bytes = pdf_service.generate_pdf(
            markdown_content=cv.markdown_content or "",
            settings=cv.settings
        )
        
        # Create filename
        safe_name = "".join(c for c in cv.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_name}.pdf"
        
        # Return PDF response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\"",
                "Content-Length": str(len(pdf_bytes))
            }
        )
        
    except Exception as e:
        logger.error(f"PDF generation failed for CV {cv_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF. Please check your CV content and try again."
        )

@router.get("/{cv_id}/markdown")
def download_cv_markdown(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download CV as Markdown file"""
    # Get the CV
    cv = get_cv_by_id(db, cv_id, str(current_user.id))
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    # Create filename
    safe_name = "".join(c for c in cv.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{safe_name}.md"
    
    # Return markdown content
    content = cv.markdown_content or "# Your CV\n\nPlease add your CV content here."
    
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename=\"{filename}\"",
            "Content-Length": str(len(content.encode('utf-8')))
        }
    )

@router.get("/{cv_id}/preview-pdf")
def preview_cv_pdf(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview CV as PDF (inline display)"""
    # Get the CV
    cv = get_cv_by_id(db, cv_id, str(current_user.id))
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    try:
        # Generate PDF
        pdf_bytes = pdf_service.generate_pdf(
            markdown_content=cv.markdown_content or "",
            settings=cv.settings
        )
        
        # Return PDF for inline viewing
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "inline",
                "Content-Length": str(len(pdf_bytes))
            }
        )
        
    except Exception as e:
        logger.error(f"PDF preview failed for CV {cv_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF preview. Please check your CV content and try again."
        )

# Legacy endpoint for backward compatibility
@router.get("/{cv_id}/download")
def download_cv_pdf_legacy(
    cv_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download CV as PDF (legacy endpoint)"""
    cv = get_cv_by_id(db, cv_id, str(current_user.id))
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    try:
        pdf_bytes = pdf_service.generate_pdf(cv.markdown_content, cv.settings or {})
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={cv.name.replace(' ', '_')}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF"
        )