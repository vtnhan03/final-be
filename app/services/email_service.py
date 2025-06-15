"""Email service using Resend for sending emails."""

import resend
from app.core.config import settings

# Initialize Resend
if settings.resend_api_key:
    resend.api_key = settings.resend_api_key


class EmailService:
    """Email service for sending various types of emails."""
    
    @staticmethod
    def send_welcome_email(email: str, username: str) -> bool:
        """Send welcome email to new users."""
        if not settings.resend_api_key:
            print(f"RESEND_API_KEY not configured. Mock welcome email to {email}")
            return True
        
        try:
            subject = "Welcome to ChildSafe! 🎉"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to ChildSafe</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0; color: white; }}
                    .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e9ecef; }}
                    .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #6c757d; border-radius: 0 0 8px 8px; }}
                    .feature {{ background-color: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Welcome to ChildSafe!</h1>
                        <p>Your account has been created successfully</p>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        <p>Welcome to ChildSafe! We're excited to have you on board.</p>
                        
                        <div class="feature">
                            <h3>🔒 Security Features</h3>
                            <ul>
                                <li>Set up a PIN for additional security</li>
                                <li>Change your password anytime</li>
                                <li>Secure password reset via email</li>
                            </ul>
                        </div>
                        
                        <p>Thank you for choosing ChildSafe!</p>
                    </div>
                    <div class="footer">
                        <p>&copy; 2024 ChildSafe. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            params = {
                "from": settings.from_email,
                "to": settings.to_email,
                "subject": subject,
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            print(f"Welcome email sent successfully to {email}. ID: {response.get('id')}")
            return True
            
        except Exception as e:
            print(f"Failed to send welcome email: {str(e)}")
            return False
    
    @staticmethod
    def send_reset_email(email: str, verification_code: str, reset_type: str) -> bool:
        """Send password or PIN reset email with verification code."""
        if not settings.resend_api_key:
            print(f"Mock {reset_type} reset email to {email}")
            print(f"Verification code: {verification_code}")
            return True
        
        try:
            if reset_type == "password":
                subject = "Reset Your Password - ChildSafe"
                content_title = "🔒 Password Reset Request"
                content_text = "reset your password"
            else:
                subject = "Reset Your PIN - ChildSafe"
                content_title = "🔢 PIN Reset Request"
                content_text = "reset your PIN"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{reset_type.title()} Reset</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ background-color: #ffffff; padding: 30px; border: 1px solid #e9ecef; }}
                    .code-box {{ background-color: #f8f9fa; border: 2px solid #007bff; padding: 20px; margin: 20px 0; text-align: center; border-radius: 8px; }}
                    .verification-code {{ font-size: 32px; font-weight: bold; color: #007bff; letter-spacing: 8px; font-family: 'Courier New', monospace; }}
                    .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #6c757d; border-radius: 0 0 8px 8px; }}
                    .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>{content_title}</h1>
                    </div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>We received a request to {content_text} for your ChildSafe account.</p>
                        
                        <p>Please use the following verification code:</p>
                        
                        <div class="code-box">
                            <div class="verification-code">{verification_code}</div>
                        </div>
                        
                        <p>Enter this code in the app to complete your {reset_type} reset.</p>
                        
                        <div class="warning">
                            <strong>⚠️ Important:</strong>
                            <ul>
                                <li>This code will expire in 1 hour</li>
                                <li>If you didn't request this reset, please ignore this email</li>
                                <li>Never share this code with anyone</li>
                            </ul>
                        </div>
                    </div>
                    <div class="footer">
                        <p>&copy; 2024 ChildSafe. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            params = {
                "from": settings.from_email,
                "to": settings.to_email,
                "subject": subject,
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            print(f"Reset email sent successfully to {email}. ID: {response.get('id')}")
            return True
            
        except Exception as e:
            print(f"Failed to send reset email: {str(e)}")
            return False 