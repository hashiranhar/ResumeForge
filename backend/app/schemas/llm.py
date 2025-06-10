from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Dict, Any

# Function 1: Chatbot Interface
class ChatRequest(BaseModel):
    """Chat with LLM about CV"""
    message: str  
    cv_id: Optional[UUID] = None  
    cv_content: Optional[str] = None  
    conversation_history: Optional[List[Dict[str, str]]] = []  

class ChatResponse(BaseModel):
    """Chat response from LLM"""
    success: bool
    reply: str  
    suggestions: List[str] = []  
    error: Optional[str] = None

# Function 2: Inline Editor
class InlineEditRequest(BaseModel):
    """Real-time CV editing request"""
    cv_id: UUID  
    instruction: str  
    section: Optional[str] = None  
    auto_save: bool = True  

class InlineEditResponse(BaseModel):
    """Inline edit response - just the edited content"""
    success: bool
    edited_content: str  
    changes_made: List[str] = []  
    auto_saved: bool = False  
    error: Optional[str] = None

# Function 3: ATS Score Button
class ATSAnalysisRequest(BaseModel):
    """ATS score analysis request"""
    cv_id: Optional[UUID] = None  
    cv_content: Optional[str] = None  
    target_role: Optional[str] = None 
    job_description: Optional[str] = None  

class ATSAnalysisResponse(BaseModel):
    """ATS score and recommendations"""
    success: bool
    ats_score: int  
    score_breakdown: Dict[str, int]  
    strengths: List[str]  
    weaknesses: List[str]  
    upgrade_suggestions: List[str]  
    keyword_analysis: Dict[str, Any] = {}  
    error: Optional[str] = None