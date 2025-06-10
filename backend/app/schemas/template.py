from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict, Any

class TemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    markdown_content: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    is_default: str
    
    class Config:
        from_attributes = True

class CreateCVFromTemplate(BaseModel):
    template_id: UUID
    cv_name: str