# backend/app/routers/subscription.py

import os
import stripe
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user
from app.services.subscription_service import SubscriptionService
from app.models.subscription import SubscriptionPlan
import logging

# Load Stripe keys from environment
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

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


@router.post("/checkout")
async def create_checkout_session(
    request: Request,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = await request.json()
    plan_id = data.get("plan_id")
    billing_cycle = data.get("billing_cycle", "monthly")

    # Fetch plan from DB to get Stripe price ID
    from app.models.subscription import SubscriptionPlan
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    price_id = plan.stripe_monthly_price_id if billing_cycle == "monthly" else plan.stripe_yearly_price_id
    if not price_id:
        raise HTTPException(status_code=400, detail="Stripe price ID not set for this plan/cycle")

    # Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/subscription",
            metadata={
                "user_id": str(current_user.id),
                "plan_id": str(plan_id),
            }
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": f"Webhook error: {str(e)}"})

    # Handle subscription events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: Mark subscription as active in your DB for session["customer_email"]
        # You may want to store session["subscription"] (Stripe subscription ID)
    elif event["type"] == "customer.subscription.updated":
        # TODO: Update subscription status in your DB
        pass
    elif event["type"] == "customer.subscription.deleted":
        # TODO: Mark subscription as canceled in your DB
        pass
    # Add more event types if needed

    return {"status": "success"}


@router.post("/customer-portal")
async def create_customer_portal(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch Stripe customer ID from your DB
    from app.models.user_subscription import UserSubscription
    user_sub = db.query(UserSubscription).filter(UserSubscription.user_id == current_user.id).first()
    if not user_sub or not user_sub.stripe_customer_id:
        raise HTTPException(status_code=404, detail="Stripe customer not found")

    try:
        session = stripe.billing_portal.Session.create(
            customer=user_sub.stripe_customer_id,
            return_url=f"{FRONTEND_URL}/subscription"
        )
        return {"portal_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))