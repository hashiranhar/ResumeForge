from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class CVCreate(BaseModel):
    name: str
    markdown_content: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class CVUpdate(BaseModel):
    name: Optional[str] = None
    markdown_content: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class CVResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    markdown_content: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CVListResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True