from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.llm import LLMEditRequest, LLMEditResponse, LLMSuggestionsRequest, LLMSuggestionsResponse, QuickEditRequest
from app.schemas.auth import UserResponse
from app.crud.cv import get_cv_by_id, update_cv
from app.routers.auth import get_current_user
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/llm", tags=["llm"])

@router.post("/edit", response_model=LLMEditResponse)
def edit_cv_with_llm(
    request: LLMEditRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Get current CV content
        current_content = ""
        cv_context = {}
        
        if request.cv_id:
            # Get existing CV
            cv = get_cv_by_id(db, str(request.cv_id), str(current_user.id))
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            current_content = cv.markdown_content or ""
            cv_context = {
                "cv_name": cv.name,
                "target_role": request.target_role
            }
        else:
            # Use provided content
            current_content = request.current_content or ""
            cv_context = {"target_role": request.target_role}
        
        if not current_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No CV content provided to edit"
            )
        
        # Call LLM service
        result = llm_service.edit_cv_content(
            current_content=current_content,
            user_instruction=request.instruction,
            context=cv_context
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "AI editing failed")
            )
        
        # Optionally update the CV in database
        updated_cv = None
        if request.cv_id and request.save_changes:
            updated_cv = update_cv(
                db=db,
                cv_id=str(request.cv_id),
                user_id=str(current_user.id),
                markdown_content=result["edited_content"]
            )
            if not updated_cv:
                logger.warning(f"Failed to save LLM edits to CV {request.cv_id}")
        
        return LLMEditResponse(
            success=True,
            edited_content=result["edited_content"],
            explanation=result["explanation"],
            suggestions=result.get("suggestions", []),
            cv_updated=updated_cv is not None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LLM edit endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process AI editing request"
        )

@router.post("/suggestions", response_model=LLMSuggestionsResponse)
def get_cv_suggestions(
    request: LLMSuggestionsRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Get CV content
        cv_content = ""
        
        if request.cv_id:
            cv = get_cv_by_id(db, str(request.cv_id), str(current_user.id))
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            cv_content = cv.markdown_content or ""
        else:
            cv_content = request.content or ""
        
        if not cv_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No CV content provided for analysis"
            )
        
        # Get suggestions from LLM
        result = llm_service.suggest_improvements(cv_content)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to analyze CV")
            )
        
        return LLMSuggestionsResponse(
            success=True,
            suggestions=result["suggestions"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LLM suggestions endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate CV suggestions"
        )

@router.post("/quick-edit")
def quick_edit_cv_section(
    request: QuickEditRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Get CV
        cv = get_cv_by_id(db, str(request.cv_id), str(current_user.id))
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found"
            )
        
        # Create targeted instruction
        targeted_instruction = f"Focus only on the {request.section} section and {request.instruction}"
        
        # Call LLM service
        result = llm_service.edit_cv_content(
            current_content=cv.markdown_content or "",
            user_instruction=targeted_instruction,
            context={"cv_name": cv.name, "focus_section": request.section}
        )
        
        if not result["success"]:
            return {"success": False, "error": result.get("error", "Quick edit failed")}
        
        return {
            "success": True,
            "edited_content": result["edited_content"],
            "explanation": result["explanation"],
            "section_focused": request.section
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quick edit failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform quick edit"
        )