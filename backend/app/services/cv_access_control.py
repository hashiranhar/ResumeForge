# backend/app/services/cv_access_control.py

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.cv import CV
from app.services.subscription_service import SubscriptionService
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class CVAccessControlService:
    """Service for controlling CV access based on subscription limits"""
    
    def __init__(self, db: Session):
        self.db = db
        self.subscription_service = SubscriptionService(db)
    
    def get_user_cvs_with_access_info(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's CVs with access control information
        Returns CVs marked as editable/read-only based on subscription limits
        CVs are ordered by creation date (newest first), latest N CVs are editable
        """
        try:
            # Get user's CVs ordered by creation date (NEWEST first)
            cvs = self.db.query(CV).filter(CV.user_id == user_id).order_by(CV.created_at.desc()).all()
            
            # Get user's current limits
            usage_data = self.subscription_service.get_user_current_usage(user_id)
            cv_limit = usage_data['cvs_limit']
            
            cvs_with_access = []
            for i, cv in enumerate(cvs):
                # First N CVs (newest ones) are editable, rest are read-only
                is_editable = i < cv_limit
                
                cvs_with_access.append({
                    'id': str(cv.id),
                    'user_id': str(cv.user_id),
                    'name': cv.name,
                    'markdown_content': cv.markdown_content,
                    'settings': cv.settings,
                    'created_at': cv.created_at,
                    'updated_at': cv.updated_at,
                    'is_editable': is_editable,
                    'access_type': 'edit' if is_editable else 'read_only',
                    'position': i + 1  # 1-based position (1 = newest, higher = older)
                })
            
            return cvs_with_access
            
        except Exception as e:
            logger.error(f"Error getting CVs with access info for user {user_id}: {e}")
            return []
    
    def check_cv_edit_permission(self, user_id: str, cv_id: str) -> Dict[str, Any]:
        """
        Check if user can edit a specific CV
        Returns permission info and raises exception if not allowed
        Latest CVs (by creation date) are editable up to the limit
        """
        try:
            # Get the CV
            cv = self.db.query(CV).filter(CV.id == cv_id, CV.user_id == user_id).first()
            if not cv:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found"
                )
            
            # Get user's CVs ordered by creation date (NEWEST first)
            cvs = self.db.query(CV).filter(CV.user_id == user_id).order_by(CV.created_at.desc()).all()
            
            # Find the position of this CV (1 = newest, higher = older)
            cv_position = None
            for i, user_cv in enumerate(cvs):
                if str(user_cv.id) == cv_id:
                    cv_position = i + 1  # 1-based position
                    break
            
            if cv_position is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="CV not found in user's CVs"
                )
            
            # Get user's current limits
            usage_data = self.subscription_service.get_user_current_usage(user_id)
            cv_limit = usage_data['cvs_limit']
            
            # Check if this CV is within the editable limit (newest CVs are editable)
            is_editable = cv_position <= cv_limit
            
            if not is_editable:
                # Get subscription info for error message
                subscription_data = self.subscription_service.get_user_subscription(user_id)
                plan_name = subscription_data['plan']['display_name'] if subscription_data else 'Free'
                
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": "CV editing not allowed",
                        "reason": "cv_limit_exceeded",
                        "plan": plan_name,
                        "cv_position": cv_position,
                        "editable_limit": cv_limit,
                        "access_type": "read_only",
                        "upgrade_needed": plan_name != "Pro",
                        "explanation": f"Your {plan_name} plan allows editing your {cv_limit} newest CVs. This CV is #{cv_position} (older) and is read-only. Upgrade to edit more CVs or delete some newer CVs to make this one editable."
                    }
                )
            
            return {
                "editable": True,
                "cv_position": cv_position,
                "cv_limit": cv_limit,
                "access_type": "edit"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error checking CV edit permission for user {user_id}, CV {cv_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to check CV permissions"
            )
    
    def get_cv_access_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get summary of user's CV access (for dashboard/UI)
        """
        try:
            # Get user's CVs (newest first)
            cvs = self.db.query(CV).filter(CV.user_id == user_id).order_by(CV.created_at.desc()).all()
            total_cvs = len(cvs)
            
            # Get user's limits
            usage_data = self.subscription_service.get_user_current_usage(user_id)
            cv_limit = usage_data['cvs_limit']
            
            editable_cvs = min(total_cvs, cv_limit)
            read_only_cvs = max(0, total_cvs - cv_limit)
            
            return {
                "total_cvs": total_cvs,
                "editable_cvs": editable_cvs,
                "read_only_cvs": read_only_cvs,
                "cv_limit": cv_limit,
                "over_limit": total_cvs > cv_limit,
                "can_create_new": total_cvs < cv_limit
            }
            
        except Exception as e:
            logger.error(f"Error getting CV access summary for user {user_id}: {e}")
            return {
                "total_cvs": 0,
                "editable_cvs": 0,
                "read_only_cvs": 0,
                "cv_limit": 3,  # Default free limit
                "over_limit": False,
                "can_create_new": True
            }