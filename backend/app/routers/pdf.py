from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user
from app.services.pdf_service import pdf_service
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pdf", tags=["pdf"])
    
@router.post("/create-cv", response_model=dict)
async def create_cv_from_pdf(
    file: UploadFile = File(...),
    cv_name: str = Form(...),
    preferences: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 3: Convert PDF to markdown and directly create a new CV
    """
    try:
        # Extract text
        file_content = await file.read()
        extraction_result = pdf_service.extract_text_from_pdf(file_content)
        
        if not extraction_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to extract text: {extraction_result['error']}"
            )
        
        # Convert to markdown using AI
        user_prefs = {"style": preferences} if preferences else None
        conversion_result = llm_service.pdf_to_markdown(
            pdf_text=extraction_result["text"],
            user_preferences=user_prefs
        )
        
        if not conversion_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI conversion failed: {conversion_result['error']}"
            )
        
        # Create new CV with the generated markdown
        from app.crud.cv import create_cv
        
        new_cv = create_cv(
            db=db,
            user_id=str(current_user.id),
            name=cv_name,
            markdown_content=conversion_result["markdown"],
            settings={
                "font": "Arial",
                "fontSize": 11,
                "margins": {"top": 20, "bottom": 20, "left": 15, "right": 15},
                "theme": "professional"
            }
        )
        
        if not new_cv:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create CV"
            )
        
        return {
            "success": True,
            "cv": {
                "id": str(new_cv.id),
                "name": new_cv.name,
                "markdown_content": new_cv.markdown_content,
                "settings": new_cv.settings,
                "created_at": new_cv.created_at.isoformat(),
                "updated_at": new_cv.updated_at.isoformat()
            },
            "processing_info": {
                "original_filename": file.filename,
                "processing_method": extraction_result.get("method", "unknown"),
                "suggestions": [
                    "CV created successfully from PDF",
                    "Review and edit the content as needed",
                    "Customize formatting and sections",
                    "Add any missing information"
                ]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF to CV creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create CV from PDF"
        )