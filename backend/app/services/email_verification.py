import smtplib
import random
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings
from app.models.user import User
from app.crud.user import get_user_by_email
import logging

logger = logging.getLogger(__name__)

class EmailVerificationService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.sender_email = settings.sender_email
        self.sender_password = settings.sender_password
        self.verification_code_expire_minutes = 15  # 15 minutes expiry
        self.max_attempts = 3  # Maximum verification attempts
    
    def generate_verification_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_email(self, email: str, verification_code: str) -> bool:
        """Send verification email with code"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Verify your email - ResumeForge"
            message["From"] = self.sender_email
            message["To"] = email
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Verification</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333;">
                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="min-height: 100vh; background-color: #f7fafc;">
                    <tr>
                        <td align="center" style="padding: 40px 20px;">
                            <table cellpadding="0" cellspacing="0" border="0" width="600" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); overflow: hidden;">
                                <!-- Header -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); padding: 40px; text-align: center;">
                                        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                                            📧 Verify Your Email
                                        </h1>
                                        <p style="color: #e0e7ff; margin: 8px 0 0; font-size: 18px; opacity: 0.9;">
                                            Welcome to ResumeForge!
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Content -->
                                <tr>
                                    <td style="padding: 40px;">
                                        <p style="color: #374151; margin: 0 0 24px; font-size: 16px; line-height: 1.6;">
                                            Hi there! 👋
                                        </p>
                                        
                                        <p style="color: #374151; margin: 0 0 32px; font-size: 16px; line-height: 1.6;">
                                            Thanks for signing up for ResumeForge! To complete your registration and start creating amazing resumes, please enter the verification code below:
                                        </p>
                                        
                                        <!-- Verification Code -->
                                        <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border-radius: 12px; padding: 32px; text-align: center; margin: 32px 0; border: 2px dashed #9ca3af;">
                                            <p style="color: #6b7280; margin: 0 0 16px; font-size: 14px; font-weight: 500; text-transform: uppercase; letter-spacing: 1px;">
                                                Your Verification Code
                                            </p>
                                            <div style="font-size: 36px; font-weight: 800; color: #2563eb; font-family: 'Courier New', monospace; letter-spacing: 8px; text-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);">
                                                {verification_code}
                                            </div>
                                        </div>
                                        
                                        <p style="color: #374151; margin: 24px 0; font-size: 16px; line-height: 1.6;">
                                            Enter this code on the verification page to activate your account. This code will expire in <strong>15 minutes</strong> for security reasons.
                                        </p>
                                        
                                        <!-- Security Notice -->
                                        <div style="background-color: #fef5e7; border-left: 4px solid #f6ad55; padding: 20px; margin: 32px 0; border-radius: 0 8px 8px 0;">
                                            <p style="color: #744210; margin: 0; font-size: 14px; font-weight: 500;">
                                                🔒 <strong>Security Notice:</strong><br>
                                                If you didn't create an account with ResumeForge, please ignore this email. Your email address will not be used for any other purposes.
                                            </p>
                                        </div>
                                        
                                        <p style="color: #6b7280; margin: 32px 0 0; font-size: 14px; line-height: 1.6;">
                                            Need help? Our support team is here to assist you.
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: #f7fafc; padding: 30px 40px; border-top: 1px solid #e2e8f0;">
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                            <tr>
                                                <td style="text-align: center;">
                                                    <p style="color: #718096; margin: 0 0 16px; font-size: 14px;">
                                                        Welcome to the ResumeForge community! 🚀
                                                    </p>
                                                    <p style="color: #a0aec0; margin: 0; font-size: 12px; line-height: 1.5;">
                                                        © 2024 ResumeForge. All rights reserved.<br>
                                                        This email was sent to help you verify your account.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            # Create plain text version
            text_content = f"""
            Verify Your Email - ResumeForge
            
            Hi there!
            
            Thanks for signing up for ResumeForge! To complete your registration, please enter this verification code:
            
            {verification_code}
            
            This code will expire in 15 minutes for security reasons.
            
            If you didn't create an account with ResumeForge, please ignore this email.
            
            Welcome to ResumeForge!
            """
            
            # Create MIMEText objects
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")
            
            # Add parts to message
            message.attach(text_part)
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, email, message.as_string())
            
            logger.info(f"Verification email sent successfully to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            return False
    
    def create_verification_code(self, db: Session, user: User) -> str:
        """Create and store verification code for user"""
        verification_code = self.generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=self.verification_code_expire_minutes)
        
        # Update user with verification code
        user.verification_code = verification_code
        user.verification_code_expires = expires_at
        user.verification_attempts = 0
        
        db.commit()
        db.refresh(user)
        
        return verification_code
    
    def verify_code(self, db: Session, email: str, code: str) -> dict:
        """Verify the submitted code"""
        user = get_user_by_email(db, email)
        
        if not user:
            return {"success": False, "error": "User not found"}
        
        if user.email_verified:
            return {"success": False, "error": "Email already verified"}
        
        if not user.verification_code:
            return {"success": False, "error": "No verification code found"}
        
        if user.verification_code_expires < datetime.utcnow():
            return {"success": False, "error": "Verification code expired"}
        
        if user.verification_attempts >= self.max_attempts:
            return {"success": False, "error": "Maximum verification attempts exceeded"}
        
        if user.verification_code != code:
            # Increment attempts
            user.verification_attempts += 1
            db.commit()
            
            remaining_attempts = self.max_attempts - user.verification_attempts
            if remaining_attempts > 0:
                return {
                    "success": False, 
                    "error": f"Invalid verification code. {remaining_attempts} attempts remaining"
                }
            else:
                return {"success": False, "error": "Maximum verification attempts exceeded"}
        
        # Code is valid - mark email as verified
        user.email_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        user.verification_attempts = 0
        
        db.commit()
        db.refresh(user)
        
        return {"success": True, "message": "Email verified successfully"}
    
    def resend_verification_code(self, db: Session, email: str) -> dict:
        """Resend verification code to user"""
        user = get_user_by_email(db, email)
        
        if not user:
            return {"success": False, "error": "User not found"}
        
        if user.email_verified:
            return {"success": False, "error": "Email already verified"}
        
        # Reset attempts when resending
        user.verification_attempts = 0
        
        # Create new verification code
        verification_code = self.create_verification_code(db, user)
        
        # Send email
        if self.send_verification_email(email, verification_code):
            return {"success": True, "message": "Verification code sent successfully"}
        else:
            return {"success": False, "error": "Failed to send verification email"}

# Create singleton instance
email_verification_service = EmailVerificationService()