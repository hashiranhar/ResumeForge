# backend/app/routers/subscription.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user
from app.services.subscription_service import SubscriptionService
from app.models.subscription import SubscriptionPlan
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/subscription", tags=["subscription"])


@router.get("/plans")
def get_subscription_plans(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get all available subscription plans
    """
    try:
        plans = db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()
        
        plans_data = []
        for plan in plans:
            plans_data.append({
                "id": plan.id,
                "name": plan.name,
                "display_name": plan.display_name,
                "description": plan.description,
                "monthly_price_pennies": plan.monthly_price_pennies,
                "yearly_price_pennies": plan.yearly_price_pennies,
                "monthly_price_pounds": plan.monthly_price_pennies / 100,
                "yearly_price_pounds": plan.yearly_price_pennies / 100,
                "api_calls_per_day": plan.api_calls_per_day,
                "max_cvs": plan.max_cvs,
                "features": {
                    "api_calls_per_day": plan.api_calls_per_day,
                    "max_cvs": plan.max_cvs,
                    "chat_support": plan.name != "free",
                    "premium_templates": plan.name == "pro",
                    "priority_processing": plan.name == "pro"
                }
            })
        
        return {
            "success": True,
            "plans": plans_data
        }
        
    except Exception as e:
        logger.error(f"Error fetching subscription plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch subscription plans"
        )


@router.get("/current")
def get_current_subscription(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's current subscription details
    """
    try:
        service = SubscriptionService(db)
        subscription_data = service.get_user_subscription(str(current_user.id))
        
        if not subscription_data:
            # User has no subscription, return free tier info
            free_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.name == "free").first()
            if not free_plan:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Free plan not found in database"
                )
            
            return {
                "success": True,
                "has_subscription": False,
                "subscription": None,
                "plan": {
                    "id": free_plan.id,
                    "name": free_plan.name,
                    "display_name": free_plan.display_name,
                    "api_calls_per_day": free_plan.api_calls_per_day,
                    "max_cvs": free_plan.max_cvs,
                    "monthly_price_pennies": free_plan.monthly_price_pennies,
                    "yearly_price_pennies": free_plan.yearly_price_pennies
                }
            }
        
        return {
            "success": True,
            "has_subscription": True,
            "subscription": {
                "id": subscription_data["subscription_id"],
                "status": subscription_data["status"],
                "billing_cycle": subscription_data["billing_cycle"],
                "current_period_start": subscription_data["current_period_start"].isoformat() if subscription_data["current_period_start"] else None,
                "current_period_end": subscription_data["current_period_end"].isoformat() if subscription_data["current_period_end"] else None,
                "cancel_at_period_end": subscription_data["cancel_at_period_end"]
            },
            "plan": subscription_data["plan"]
        }
        
    except Exception as e:
        logger.error(f"Error fetching current subscription for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch current subscription"
        )


@router.get("/usage")
def get_usage_info(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's current usage and limits
    """
    try:
        service = SubscriptionService(db)
        usage_data = service.get_user_current_usage(str(current_user.id))
        
        # Calculate percentages for frontend progress bars
        api_usage_percentage = (usage_data["api_calls_used"] / usage_data["api_calls_limit"]) * 100 if usage_data["api_calls_limit"] > 0 else 0
        cv_usage_percentage = (usage_data["cvs_used"] / usage_data["cvs_limit"]) * 100 if usage_data["cvs_limit"] > 0 else 0
        
        # Determine warning levels
        api_warning_level = "high" if api_usage_percentage >= 90 else "medium" if api_usage_percentage >= 70 else "low"
        cv_warning_level = "high" if cv_usage_percentage >= 90 else "medium" if cv_usage_percentage >= 70 else "low"
        
        return {
            "success": True,
            "usage": {
                "api_calls": {
                    "used": usage_data["api_calls_used"],
                    "limit": usage_data["api_calls_limit"],
                    "remaining": usage_data["api_calls_remaining"],
                    "percentage": round(api_usage_percentage, 1),
                    "warning_level": api_warning_level
                },
                "cvs": {
                    "used": usage_data["cvs_used"],
                    "limit": usage_data["cvs_limit"],
                    "remaining": usage_data["cvs_remaining"],
                    "percentage": round(cv_usage_percentage, 1),
                    "warning_level": cv_warning_level
                },
                "usage_date": usage_data["usage_date"],
                "reset_info": "API calls reset daily at midnight UK time"
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching usage info for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch usage information"
        )


@router.get("/dashboard")
def get_subscription_dashboard(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get complete subscription dashboard data (combines subscription + usage + plans)
    """
    try:
        service = SubscriptionService(db)
        
        # Get current subscription
        subscription_data = service.get_user_subscription(str(current_user.id))
        
        # Get usage info
        usage_data = service.get_user_current_usage(str(current_user.id))
        
        # Get available plans for upgrade options
        plans = db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()
        
        # Calculate usage percentages
        api_usage_percentage = (usage_data["api_calls_used"] / usage_data["api_calls_limit"]) * 100 if usage_data["api_calls_limit"] > 0 else 0
        cv_usage_percentage = (usage_data["cvs_used"] / usage_data["cvs_limit"]) * 100 if usage_data["cvs_limit"] > 0 else 0
        
        # Determine if user should be prompted to upgrade
        should_upgrade = False
        upgrade_reason = None
        
        if usage_data["api_calls_remaining"] <= 1:
            should_upgrade = True
            upgrade_reason = "api_limit_reached"
        elif usage_data["cvs_remaining"] <= 0:
            should_upgrade = True
            upgrade_reason = "cv_limit_reached"
        elif api_usage_percentage >= 80:
            should_upgrade = True
            upgrade_reason = "api_limit_approaching"
        elif cv_usage_percentage >= 80:
            should_upgrade = True
            upgrade_reason = "cv_limit_approaching"
        
        # Current plan info
        if subscription_data:
            current_plan = subscription_data["plan"]
        else:
            free_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.name == "free").first()
            current_plan = {
                "name": free_plan.name,
                "display_name": free_plan.display_name,
                "api_calls_per_day": free_plan.api_calls_per_day,
                "max_cvs": free_plan.max_cvs
            }
        
        # Available upgrade options (exclude current plan)
        upgrade_options = []
        for plan in plans:
            if plan.name != current_plan["name"]:
                upgrade_options.append({
                    "id": plan.id,
                    "name": plan.name,
                    "display_name": plan.display_name,
                    "monthly_price_pennies": plan.monthly_price_pennies,
                    "yearly_price_pennies": plan.yearly_price_pennies,
                    "monthly_price_pounds": plan.monthly_price_pennies / 100,
                    "yearly_price_pounds": plan.yearly_price_pennies / 100,
                    "api_calls_per_day": plan.api_calls_per_day,
                    "max_cvs": plan.max_cvs
                })
        
        return {
            "success": True,
            "current_plan": current_plan,
            "subscription": subscription_data,
            "usage": {
                "api_calls": {
                    "used": usage_data["api_calls_used"],
                    "limit": usage_data["api_calls_limit"],
                    "remaining": usage_data["api_calls_remaining"],
                    "percentage": round(api_usage_percentage, 1)
                },
                "cvs": {
                    "used": usage_data["cvs_used"],
                    "limit": usage_data["cvs_limit"],
                    "remaining": usage_data["cvs_remaining"],
                    "percentage": round(cv_usage_percentage, 1)
                }
            },
            "upgrade_prompt": {
                "should_upgrade": should_upgrade,
                "reason": upgrade_reason,
                "options": upgrade_options
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching subscription dashboard for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch subscription dashboard"
        )