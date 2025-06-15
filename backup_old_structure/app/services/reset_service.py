"""Reset service for password and PIN reset functionality."""

import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User, ResetToken
from app.utils import generate_reset_token, get_password_hash, get_pin_hash, validate_password, validate_pin
from app.services.email_service import EmailService
from app.services.user_service import UserService


class ResetService:
    """Service class for reset-related operations."""
    
    @staticmethod
    def create_reset_token(db: Session, user_id: int, token_type: str) -> str:
        """Create a reset token in the database."""
        token = generate_reset_token()
        expires_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat()
        
        reset_token = ResetToken(
            user_id=user_id,
            token=token,
            token_type=token_type,
            expires_at=expires_at,
            used=False
        )
        
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)
        
        return token
    
    @staticmethod
    def verify_reset_token(db: Session, token: str, token_type: str) -> ResetToken:
        """Verify and return the reset token if valid."""
        reset_token = db.query(ResetToken).filter(
            ResetToken.token == token,
            ResetToken.token_type == token_type,
            ResetToken.used == False
        ).first()
        
        if not reset_token:
            return None
        
        # Check if token is expired
        expires_at = datetime.datetime.fromisoformat(reset_token.expires_at)
        if datetime.datetime.utcnow() > expires_at:
            return None
        
        return reset_token
    
    @staticmethod
    def mark_token_as_used(db: Session, token: str) -> None:
        """Mark a reset token as used."""
        reset_token = db.query(ResetToken).filter(ResetToken.token == token).first()
        if reset_token:
            reset_token.used = True
            db.commit()
    
    @staticmethod
    def request_password_reset(db: Session, email: str) -> str:
        """Request password reset."""
        user = UserService.get_user_by_email(db, email)
        if not user:
            # Don't reveal if email exists for security
            return "If the email exists, a password reset link has been sent"
        
        # Check if user is a Google user
        if user.is_google_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account uses Google authentication. Please sign in with Google."
            )
        
        # Generate reset token
        token = ResetService.create_reset_token(db, user.id, "password")
        
        # Send email
        EmailService.send_reset_email(email, token, "password")
        
        return "If the email exists, a password reset link has been sent"
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> str:
        """Reset password using token."""
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Verify reset token
        reset_token = ResetService.verify_reset_token(db, token, "password")
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Get user and update password
        user = db.query(User).filter(User.id == reset_token.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.hashed_password = get_password_hash(new_password)
        
        # Mark token as used
        ResetService.mark_token_as_used(db, token)
        
        db.commit()
        
        return "Password has been reset successfully"
    
    @staticmethod
    def request_pin_reset(db: Session, email: str) -> str:
        """Request PIN reset."""
        user = UserService.get_user_by_email(db, email)
        if not user or not user.hashed_pin:
            # Don't reveal if email exists or has PIN for security
            return "If the email exists and has a PIN set, a PIN reset link has been sent"
        
        # Generate reset token
        token = ResetService.create_reset_token(db, user.id, "pin")
        
        # Send email
        EmailService.send_reset_email(email, token, "pin")
        
        return "If the email exists and has a PIN set, a PIN reset link has been sent"
    
    @staticmethod
    def reset_pin(db: Session, token: str, new_pin: str) -> str:
        """Reset PIN using token."""
        # Validate new PIN
        is_valid, message = validate_pin(new_pin)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Verify reset token
        reset_token = ResetService.verify_reset_token(db, token, "pin")
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Get user and update PIN
        user = db.query(User).filter(User.id == reset_token.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.hashed_pin = get_pin_hash(new_pin)
        
        # Mark token as used
        ResetService.mark_token_as_used(db, token)
        
        db.commit()
        
        return "PIN has been reset successfully" 