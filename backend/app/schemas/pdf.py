from pydantic import BaseModel
from typing import Optional, Dict, Any

class PDFImportResponse(BaseModel):
    success: bool
    markdown_content: str
    original_filename: str
    processing_method: str
    suggestions: Optional[list] = []
    error: Optional[str] = None

class PDFAnalysisResponse(BaseModel):
    success: bool
    extracted_text: str
    text_length: int
    processing_method: str
    quality_score: int  # 1-10 based on extraction quality
    error: Optional[str] = None