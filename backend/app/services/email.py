import smtplib
from fastapi import HTTPException
from app.core.config import settings

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import os
from app.core.config import settings

def send_reset_email(email: str, reset_link: str):
    """Send password reset email to user"""
    
    # GoDaddy SMTP configuration
    smtp_server = f"{settings.smtp_server}"
    smtp_port = settings.smtp_port  
    
    # Your GoDaddy email credentials
    sender_email = settings.sender_email
    sender_password = settings.sender_password
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset your ResumeForge password"
    message["From"] = sender_email
    message["To"] = email
    
    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password - ResumeForge</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; line-height: 1.6;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f8fafc; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table cellpadding="0" cellspacing="0" border="0" width="600" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); padding: 40px 40px 30px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.5px;">
                                    📄 ResumeForge
                                </h1>
                                <p style="color: #dbeafe; margin: 8px 0 0; font-size: 16px; opacity: 0.9;">
                                    Professional Resume Builder
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Main Content -->
                        <tr>
                            <td style="padding: 50px 40px 40px;">
                                <h2 style="color: #1a202c; margin: 0 0 24px; font-size: 28px; font-weight: 600; text-align: center;">
                                    Reset Your Password
                                </h2>
                                
                                <p style="color: #4a5568; margin: 0 0 32px; font-size: 16px; text-align: center; line-height: 1.7;">
                                    We received a request to reset the password for your ResumeForge account. 
                                    Click the button below to create a new password.
                                </p>
                                
                                <!-- CTA Button -->
                                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                    <tr>
                                        <td align="center" style="padding: 20px 0;">
                                            <a href="{reset_link}" 
                                               style="display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); 
                                                      color: #ffffff; text-decoration: none; padding: 16px 40px; 
                                                      border-radius: 8px; font-weight: 600; font-size: 16px; 
                                                      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
                                                      transition: transform 0.2s ease;">
                                                🔐 Reset My Password
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Alternative Link -->
                                <p style="color: #718096; margin: 32px 0 0; font-size: 14px; text-align: center; line-height: 1.6;">
                                    Button not working? Copy and paste this link into your browser:<br>
                                    <a href="{reset_link}" style="color: #2563eb; word-break: break-all; font-size: 13px;">
                                        {reset_link}
                                    </a>
                                </p>
                                
                                <!-- Security Notice -->
                                <div style="background-color: #fef5e7; border-left: 4px solid #f6ad55; padding: 20px; margin: 32px 0; border-radius: 0 8px 8px 0;">
                                    <p style="color: #744210; margin: 0; font-size: 14px; font-weight: 500;">
                                        🔒 <strong>Security Notice:</strong><br>
                                        This link will expire in <strong>15 minutes</strong> for your security. 
                                        If you didn't request this reset, you can safely ignore this email.
                                    </p>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f7fafc; padding: 30px 40px; border-top: 1px solid #e2e8f0;">
                                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                    <tr>
                                        <td style="text-align: center;">
                                            <p style="color: #718096; margin: 0 0 16px; font-size: 14px;">
                                                Need help? Contact our support team
                                            </p>
                                            <p style="color: #a0aec0; margin: 0; font-size: 12px; line-height: 1.5;">
                                                © 2024 ResumeForge. All rights reserved.<br>
                                                This email was sent to help you access your account securely.
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
    
    # Create the plain text content
    text_content = f"""
    Reset Your Password
    
    You requested to reset your password. Click the link below to reset it:
    
    {reset_link}
    
    If you did not request this, please ignore this email.
    This link will expire in 15 minutes.
    """
    
    # Create MIMEText objects
    text_part = MIMEText(text_content, "plain")
    html_part = MIMEText(html_content, "html")
    
    # Add parts to message
    message.attach(text_part)
    message.attach(html_part)
    
    try:
        # Connect to server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            
        print(f"Password reset email sent successfully to {email}")
        
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication failed - check your email credentials")
        raise HTTPException(status_code=500, detail="Email configuration error")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")