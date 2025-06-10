from sqlalchemy.orm import Session
from app.models.cv import Template
from typing import List, Optional
from uuid import UUID

def get_all_templates(db: Session) -> List[Template]:
    """Get all available templates"""
    return db.query(Template).all()

def get_template_by_id(db: Session, template_id: str) -> Optional[Template]:
    """Get a specific template by ID"""
    return db.query(Template).filter(Template.id == template_id).first()

def get_default_templates(db: Session) -> List[Template]:
    """Get only default templates"""
    return db.query(Template).filter(Template.is_default == "true").all()