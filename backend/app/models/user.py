from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship to CVs
    cvs = relationship("CV", back_populates="user", cascade="all, delete-orphan")

    # Relationship to subscriptions, api usage, and payment history
    subscription = relationship("UserSubscription", back_populates="user", uselist=False) 
    api_usage = relationship("ApiUsage", back_populates="user", cascade="all, delete-orphan")
    payment_history = relationship("PaymentHistory", back_populates="user", cascade="all, delete-orphan")