from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.llm import ChatRequest, ChatResponse, InlineEditRequest, InlineEditResponse, ATSAnalysisRequest, ATSAnalysisResponse
from app.schemas.auth import UserResponse
from app.crud.cv import get_cv_by_id, update_cv
from app.routers.auth import get_current_user
from app.services.llm_service import llm_service
from app.services.rate_limiting_service import check_api_rate_limit
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/llm", tags=["llm"])

@router.post("/chat", response_model=ChatResponse)
def chat_about_cv(
    request: ChatRequest,
    rate_limit_check = Depends(check_api_rate_limit("chat")),  # Rate limiting added
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Function 1: Chatbot interface - User talks to LLM about their CV.
    Returns only conversational response, no content edits.
    """
    try:
        # Get CV content for context
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
            cv_content = request.cv_content or ""
        
        # Call LLM service for chat response
        result = llm_service.chat_about_cv(
            cv_content=cv_content,
            user_message=request.message,
            conversation_history=request.conversation_history or []
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Chat failed")
            )
        
        return ChatResponse(
            success=True,
            reply=result["reply"],
            suggestions=result.get("suggestions", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )

@router.post("/inline-edit", response_model=InlineEditResponse)
def inline_edit_cv(
    request: InlineEditRequest,
    rate_limit_check = Depends(check_api_rate_limit("suggestion")),  # Rate limiting added
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Function 2: Inline editor - User asks for changes, LLM edits markdown in real-time.
    Returns only the edited content, no explanations.
    """
    try:
        # Get CV
        cv = get_cv_by_id(db, str(request.cv_id), str(current_user.id))
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found"
            )
        
        # Call LLM service for inline editing
        result = llm_service.inline_edit_content(
            current_content=cv.markdown_content or "",
            edit_instruction=request.instruction,
            focus_section=request.section
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Inline edit failed")
            )
        
        # Auto-save if requested
        updated_cv = None
        if request.auto_save:
            updated_cv = update_cv(
                db=db,
                cv_id=str(request.cv_id),
                user_id=str(current_user.id),
                markdown_content=result["edited_content"]
            )
        
        return InlineEditResponse(
            success=True,
            edited_content=result["edited_content"],
            changes_made=result.get("changes_made", []),
            auto_saved=updated_cv is not None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Inline edit endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform inline edit"
        )

@router.post("/ats-score", response_model=ATSAnalysisResponse)
def get_ats_score(
    request: ATSAnalysisRequest,
    rate_limit_check = Depends(check_api_rate_limit("ats_analysis")),  # Rate limiting added
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Function 3: ATS Score Button - Analyzes CV and provides ATS score + upgrade suggestions.
    """
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
            cv_content = request.cv_content or ""
        
        if not cv_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No CV content provided for ATS analysis"
            )
        
        # Call LLM service for ATS analysis
        result = llm_service.analyze_ats_score(
            cv_content=cv_content,
            target_role=request.target_role,
            job_description=request.job_description
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "ATS analysis failed")
            )
        
        return ATSAnalysisResponse(
            success=True,
            ats_score=result["ats_score"],
            score_breakdown=result["score_breakdown"],
            strengths=result["strengths"],
            weaknesses=result["weaknesses"],
            upgrade_suggestions=result["upgrade_suggestions"],
            keyword_analysis=result.get("keyword_analysis", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ATS analysis endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform ATS analysis"
        )