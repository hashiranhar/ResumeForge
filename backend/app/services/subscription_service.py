from datetime import datetime, date
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..database import get_db
from ..models.user import User
from ..models.cv import CV
from ..models.subscription import SubscriptionPlan
from ..models.subscription import UserSubscription, ApiUsage, PaymentHistory
import logging

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Service for handling subscription-related database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user's current active subscription with plan details
        Returns None if user has no subscription
        """
        try:
            result = self.db.query(
                UserSubscription, SubscriptionPlan
            ).join(
                SubscriptionPlan, UserSubscription.plan_id == SubscriptionPlan.id
            ).filter(
                and_(
                    UserSubscription.user_id == user_id,
                    UserSubscription.status == 'active'
                )
            ).first()
            
            if not result:
                return None
                
            subscription, plan = result
            
            return {
                'subscription_id': subscription.id,
                'plan': {
                    'id': plan.id,
                    'name': plan.name,
                    'display_name': plan.display_name,
                    'api_calls_per_day': plan.api_calls_per_day,
                    'max_cvs': plan.max_cvs,
                    'monthly_price_pennies': plan.monthly_price_pennies,
                    'yearly_price_pennies': plan.yearly_price_pennies
                },
                'billing_cycle': subscription.billing_cycle,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'stripe_customer_id': subscription.stripe_customer_id,
                'stripe_subscription_id': subscription.stripe_subscription_id
            }
            
        except Exception as e:
            logger.error(f"Error getting user subscription for {user_id}: {e}")
            return None
    
    def get_user_current_usage(self, user_id: str, usage_date: Optional[date] = None) -> Dict[str, int]:
        """
        Get user's current usage for a specific date (defaults to today)
        Returns usage counts and limits
        """
        if usage_date is None:
            usage_date = date.today()
            
        try:
            # Get today's API usage
            api_usage = self.db.query(ApiUsage).filter(
                and_(
                    ApiUsage.user_id == user_id,
                    ApiUsage.usage_date == usage_date
                )
            ).first()
            
            # Count user's total CVs
            total_cvs = self.db.query(CV).filter(CV.user_id == user_id).count()
            
            # Get subscription limits
            subscription_data = self.get_user_subscription(user_id)
            if not subscription_data:
                # User has no subscription, default to free limits
                daily_limit = 5
                cv_limit = 3
            else:
                daily_limit = subscription_data['plan']['api_calls_per_day']
                cv_limit = subscription_data['plan']['max_cvs']
            
            current_api_calls = api_usage.api_calls_count if api_usage else 0
            
            return {
                'api_calls_used': current_api_calls,
                'api_calls_limit': daily_limit,
                'api_calls_remaining': max(0, daily_limit - current_api_calls),
                'cvs_used': total_cvs,
                'cvs_limit': cv_limit,
                'cvs_remaining': max(0, cv_limit - total_cvs),
                'usage_date': usage_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting usage for user {user_id}: {e}")
            # Return safe defaults on error
            return {
                'api_calls_used': 0,
                'api_calls_limit': 5,  # Free tier default
                'api_calls_remaining': 5,
                'cvs_used': 0,
                'cvs_limit': 3,  # Free tier default
                'cvs_remaining': 3,
                'usage_date': usage_date.isoformat()
            }
    
    def increment_api_usage(self, user_id: str, endpoint_type: str = 'general') -> bool:
        """
        Increment user's API usage for today
        Returns True if successful, False if failed
        """
        try:
            today = date.today()
            
            # Get or create today's usage record
            api_usage = self.db.query(ApiUsage).filter(
                and_(
                    ApiUsage.user_id == user_id,
                    ApiUsage.usage_date == today
                )
            ).first()
            
            if not api_usage:
                # Create new usage record for today
                api_usage = ApiUsage(
                    user_id=user_id,
                    usage_date=today,
                    api_calls_count=1
                )
                # Set the specific endpoint counter
                if endpoint_type == 'chat':
                    api_usage.chat_calls = 1
                elif endpoint_type == 'pdf_processing':
                    api_usage.pdf_processing_calls = 1
                elif endpoint_type == 'ats_analysis':
                    api_usage.ats_analysis_calls = 1
                elif endpoint_type == 'suggestion':
                    api_usage.suggestion_calls = 1
                
                self.db.add(api_usage)
            else:
                # Increment existing usage
                api_usage.api_calls_count += 1
                
                # Increment specific endpoint counter
                if endpoint_type == 'chat':
                    api_usage.chat_calls += 1
                elif endpoint_type == 'pdf_processing':
                    api_usage.pdf_processing_calls += 1
                elif endpoint_type == 'ats_analysis':
                    api_usage.ats_analysis_calls += 1
                elif endpoint_type == 'suggestion':
                    api_usage.suggestion_calls += 1
                
                api_usage.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error incrementing API usage for user {user_id}: {e}")
            self.db.rollback()
            return False
    
    def check_api_limit(self, user_id: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if user has reached their daily API limit
        Returns (can_proceed, limit_info)
        """
        try:
            usage_data = self.get_user_current_usage(user_id)
            can_proceed = usage_data['api_calls_remaining'] > 0
            
            return can_proceed, {
                'limit_reached': not can_proceed,
                'calls_used': usage_data['api_calls_used'],
                'calls_limit': usage_data['api_calls_limit'],
                'calls_remaining': usage_data['api_calls_remaining']
            }
            
        except Exception as e:
            logger.error(f"Error checking API limit for user {user_id}: {e}")
            # Fail safe - allow the call but log the error
            return True, {'error': 'Could not check limits'}


def get_subscription_service(db: Session = None) -> SubscriptionService:
    """Dependency function to get subscription service instance"""
    if db is None:
        db = next(get_db())
    return SubscriptionService(db)