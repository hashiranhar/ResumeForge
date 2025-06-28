from pydantic import BaseModel
from typing import Optional, Dict, Any

class CreateCVFromPDFResponse(BaseModel):
    success: bool
    cv: Dict[str, Any]
    processing_info: Dict[str, Any]
    error: Optional[str] = None