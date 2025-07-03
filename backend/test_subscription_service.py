# backend/test_subscription_service.py
# Run this script to test the subscription service

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db
from app.services.subscription_service import SubscriptionService
from app.models.user import User
from app.models.subscription import SubscriptionPlan, UserSubscription
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

def test_subscription_service():
    """Test the subscription service functions"""
    
    # Get database session
    db = next(get_db())
    service = SubscriptionService(db)
    
    print("=== Testing Subscription Service ===\n")
    
    # Test 1: Get subscription plans
    print("1. Testing subscription plans...")
    plans = db.query(SubscriptionPlan).all()
    print(f"Found {len(plans)} subscription plans:")
    for plan in plans:
        print(f"  - {plan.display_name}: {plan.api_calls_per_day} API calls/day, {plan.max_cvs} CVs max")
    
    # Test 2: Get a user for testing (first user in database)
    print("\n2. Testing with first user...")
    user = db.query(User).first()
    if not user:
        print("No users found in database. Please create a user first.")
        return
    
    print(f"Testing with user: {user.email} (ID: {user.id})")
    
    # Test 3: Get user subscription
    print("\n3. Testing get_user_subscription...")
    subscription_data = service.get_user_subscription(str(user.id))
    if subscription_data:
        print(f"User subscription found:")
        print(f"  - Plan: {subscription_data['plan']['display_name']}")
        print(f"  - Status: {subscription_data['status']}")
        print(f"  - Billing cycle: {subscription_data['billing_cycle']}")
        print(f"  - API calls per day: {subscription_data['plan']['api_calls_per_day']}")
        print(f"  - Max CVs: {subscription_data['plan']['max_cvs']}")
    else:
        print("No active subscription found for user")
    
    # Test 4: Get user usage
    print("\n4. Testing get_user_current_usage...")
    usage_data = service.get_user_current_usage(str(user.id))
    print(f"User usage:")
    print(f"  - API calls used: {usage_data['api_calls_used']}/{usage_data['api_calls_limit']}")
    print(f"  - CVs used: {usage_data['cvs_used']}/{usage_data['cvs_limit']}")
    print(f"  - API calls remaining: {usage_data['api_calls_remaining']}")
    print(f"  - CVs remaining: {usage_data['cvs_remaining']}")
    
    # Test 5: Check API limit
    print("\n5. Testing check_api_limit...")
    can_proceed, limit_info = service.check_api_limit(str(user.id))
    print(f"Can make API call: {can_proceed}")
    print(f"Limit info: {limit_info}")
    
    # Test 6: Increment API usage
    print("\n6. Testing increment_api_usage...")
    print("Incrementing API usage...")
    success = service.increment_api_usage(str(user.id), 'chat')
    print(f"Increment successful: {success}")
    
    # Check usage again
    usage_data_after = service.get_user_current_usage(str(user.id))
    print(f"Usage after increment:")
    print(f"  - API calls used: {usage_data_after['api_calls_used']}/{usage_data_after['api_calls_limit']}")
    print(f"  - API calls remaining: {usage_data_after['api_calls_remaining']}")
    
    print("\n=== Test Complete ===")
    
    # Close database session
    db.close()

if __name__ == "__main__":
    test_subscription_service()