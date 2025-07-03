# backend/app/services/rate_limiting_service.py

from functools import wraps
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.subscription_service import SubscriptionService
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)


class RateLimitExceeded(HTTPException):
    """Custom exception for rate limit exceeded"""
    def __init__(self, detail: Dict[str, Any]):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        )


class RateLimitingService:
    """Service for handling rate limiting across API endpoints"""
    
    def __init__(self, db: Session):
        self.db = db
        self.subscription_service = SubscriptionService(db)
    
    def check_and_increment_api_usage(self, user_id: str, endpoint_type: str = "general") -> Dict[str, Any]:
        """
        Check if user can make API call and increment usage if allowed
        Returns limit info or raises RateLimitExceeded
        """
        # Check if user has reached limit
        can_proceed, limit_info = self.subscription_service.check_api_limit(user_id)
        
        if not can_proceed:
            # Get user's subscription to determine response type
            subscription_data = self.subscription_service.get_user_subscription(user_id)
            
            if subscription_data:
                plan_name = subscription_data['plan']['name']
                plan_display = subscription_data['plan']['display_name']
            else:
                plan_name = 'free'
                plan_display = 'Free'
            
            # Different responses based on plan
            if plan_name == 'pro':
                # Pro users get a reset timer message
                error_detail = {
                    "message": "Daily API limit reached",
                    "plan": plan_display,
                    "upgrade_needed": False,
                    "reset_info": "Your API calls will reset at midnight UK time",
                    "current_usage": {
                        "calls_used": limit_info['calls_used'],
                        "calls_limit": limit_info['calls_limit'],
                        "calls_remaining": limit_info['calls_remaining']
                    }
                }
            else:
                # Free/Basic users get upgrade prompt
                error_detail = {
                    "message": "Daily API limit reached",
                    "plan": plan_display,
                    "upgrade_needed": True,
                    "upgrade_message": f"Upgrade to get more API calls per day",
                    "current_usage": {
                        "calls_used": limit_info['calls_used'],
                        "calls_limit": limit_info['calls_limit'],
                        "calls_remaining": limit_info['calls_remaining']
                    }
                }
            
            raise RateLimitExceeded(detail=error_detail)
        
        # Increment usage counter
        increment_success = self.subscription_service.increment_api_usage(user_id, endpoint_type)
        if not increment_success:
            logger.warning(f"Failed to increment usage for user {user_id}")
            # Continue anyway - don't block the user for logging issues
        
        return limit_info
    
    def check_cv_creation_limit(self, user_id: str) -> Dict[str, Any]:
        """
        Check if user can create a new CV
        Returns usage info or raises RateLimitExceeded
        """
        usage_data = self.subscription_service.get_user_current_usage(user_id)
        
        if usage_data['cvs_remaining'] <= 0:
            # Get user's subscription to determine response type
            subscription_data = self.subscription_service.get_user_subscription(user_id)
            
            if subscription_data:
                plan_name = subscription_data['plan']['name']
                plan_display = subscription_data['plan']['display_name']
            else:
                plan_name = 'free'
                plan_display = 'Free'
            
            error_detail = {
                "message": "CV creation limit reached",
                "plan": plan_display,
                "upgrade_needed": plan_name != 'pro',
                "upgrade_message": f"Upgrade to create more CVs" if plan_name != 'pro' else None,
                "current_usage": {
                    "cvs_used": usage_data['cvs_used'],
                    "cvs_limit": usage_data['cvs_limit'],
                    "cvs_remaining": usage_data['cvs_remaining']
                }
            }
            
            raise RateLimitExceeded(detail=error_detail)
        
        return usage_data


# FastAPI dependency functions
def check_api_rate_limit(endpoint_type: str = "general"):
    """
    FastAPI dependency to check API rate limits
    Usage: rate_limit_check = Depends(check_api_rate_limit("chat"))
    """
    def rate_limit_dependency(
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        service = RateLimitingService(db)
        return service.check_and_increment_api_usage(str(current_user.id), endpoint_type)
    
    return rate_limit_dependency


def check_cv_creation_rate_limit():
    """
    FastAPI dependency to check CV creation limits
    Usage: cv_limit_check = Depends(check_cv_creation_rate_limit())
    """
    def cv_limit_dependency(
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        service = RateLimitingService(db)
        return service.check_cv_creation_limit(str(current_user.id))
    
    return cv_limit_dependency


# Decorator versions (alternative approach)
def api_rate_limit(endpoint_type: str = "general"):
    """
    Decorator to enforce API rate limits on endpoints
    Usage: @api_rate_limit("chat")
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user and db from kwargs
            current_user = None
            db = None
            
            for key, value in kwargs.items():
                if isinstance(value, UserResponse):
                    current_user = value
                elif isinstance(value, Session):
                    db = value
            
            if not current_user or not db:
                for arg in args:
                    if isinstance(arg, UserResponse):
                        current_user = arg
                    elif isinstance(arg, Session):
                        db = arg
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User authentication required"
                )
            
            if not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session not available"
                )
            
            # Check rate limits using service
            service = RateLimitingService(db)
            service.check_and_increment_api_usage(str(current_user.id), endpoint_type)
            
            # Proceed with the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def cv_creation_limit():
    """
    Decorator to enforce CV creation limits
    Usage: @cv_creation_limit()
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user and db from kwargs
            current_user = None
            db = None
            
            for key, value in kwargs.items():
                if isinstance(value, UserResponse):
                    current_user = value
                elif isinstance(value, Session):
                    db = value
            
            if not current_user or not db:
                for arg in args:
                    if isinstance(arg, UserResponse):
                        current_user = arg
                    elif isinstance(arg, Session):
                        db = arg
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User authentication required"
                )
            
            if not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session not available"
                )
            
            # Check CV creation limits using service
            service = RateLimitingService(db)
            service.check_cv_creation_limit(str(current_user.id))
            
            # Proceed with the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator