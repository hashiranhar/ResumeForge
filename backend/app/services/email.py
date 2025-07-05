import smtplib
from fastapi import HTTPException
from app.core.config import settings

def send_reset_email(email: str, reset_link: str):
    """Send password reset email to user"""
    subject = "Reset your ResumeForge password"
    body = f"Click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, ignore this email."
    message = f"Subject: {subject}\n\n{body}"

    # EXAMPLE using SMTP, replace with actual SMTP email stuff
    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(settings.godaddy_email, settings.godaddy_password)
            server.sendmail(settings.godaddy_email, email, message)
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")
