from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Dict, Any

class LLMEditRequest(BaseModel):
    """Request model for LLM CV editing"""
    instruction: str 
    cv_id: Optional[UUID] = None 
    current_content: Optional[str] = None  
    target_role: Optional[str] = None  
    save_changes: bool = False  

class LLMEditResponse(BaseModel):
    """Response model for LLM CV editing"""
    success: bool
    edited_content: str  
    explanation: str  
    suggestions: List[str] = []  
    cv_updated: bool = False  
    error: Optional[str] = None

class LLMSuggestionsRequest(BaseModel):
    """Request model for getting CV improvement suggestions"""
    cv_id: Optional[UUID] = None  
    content: Optional[str] = None  

class LLMSuggestionsResponse(BaseModel):
    """Response model for CV suggestions"""
    success: bool
    suggestions: Dict[str, Any]  
    error: Optional[str] = None

class QuickEditRequest(BaseModel):
    """Request model for quick section editing"""
    cv_id: UUID
    section: str  
    instruction: str  