from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Pricing information
    monthly_price_pennies = Column(Integer, nullable=False, default=0)
    yearly_price_pennies = Column(Integer, nullable=False, default=0)
    
    # Usage limits
    api_calls_per_day = Column(Integer, nullable=False, default=0)
    max_cvs = Column(Integer, nullable=False, default=0)
    
    # Stripe integration
    stripe_monthly_price_id = Column(String(255))
    stripe_yearly_price_id = Column(String(255))
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_subscriptions = relationship("UserSubscription", back_populates="plan")


# backend/app/models/user_subscription.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id", ondelete="RESTRICT"), nullable=False)
    
    # Billing information
    billing_cycle = Column(String(20), nullable=False, default="monthly")
    status = Column(String(20), nullable=False, default="active")
    
    # Subscription period tracking
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    
    # Stripe integration fields
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    
    # Cancellation tracking
    cancel_at_period_end = Column(Boolean, default=False)
    cancelled_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscription")
    plan = relationship("SubscriptionPlan", back_populates="user_subscriptions")
    payment_history = relationship("PaymentHistory", back_populates="subscription")


# backend/app/models/api_usage.py
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class ApiUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Date tracking
    usage_date = Column(Date, nullable=False)
    
    # Usage counters
    api_calls_count = Column(Integer, nullable=False, default=0)
    
    # Breakdown by endpoint type
    chat_calls = Column(Integer, nullable=False, default=0)
    pdf_processing_calls = Column(Integer, nullable=False, default=0)
    ats_analysis_calls = Column(Integer, nullable=False, default=0)
    suggestion_calls = Column(Integer, nullable=False, default=0)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="api_usage")


# backend/app/models/payment_history.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class PaymentHistory(Base):
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("user_subscriptions.id", ondelete="CASCADE"), nullable=False)
    
    # Stripe payment information
    stripe_invoice_id = Column(String(255))
    stripe_payment_intent_id = Column(String(255))
    stripe_charge_id = Column(String(255))
    
    # Payment details
    amount_pennies = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False, default="GBP")
    billing_cycle = Column(String(20), nullable=False)
    
    # Payment status and timing
    status = Column(String(20), nullable=False)
    payment_date = Column(DateTime)
    due_date = Column(DateTime)
    
    # Billing period covered by this payment
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    # Additional details
    description = Column(Text)
    failure_reason = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payment_history")
    subscription = relationship("UserSubscription", back_populates="payment_history")