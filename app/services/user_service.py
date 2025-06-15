"""User service for business logic and database operations."""

import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User, ResetToken
from app.schemas import UserCreate, GoogleUser
from app.utils import (
    get_password_hash, verify_password, validate_password,
    get_pin_hash, verify_pin, validate_pin, generate_reset_token
)
from app.services.email_service import EmailService


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username already exists
        if UserService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if UserService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate password
        is_valid, message = validate_password(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            hashed_password=hashed_password,
            email=user_data.email
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Send welcome email
        EmailService.send_welcome_email(user.email, user.username)
        
        return user
    
    @staticmethod
    def create_google_user(db: Session, google_user: GoogleUser, google_id: str = None) -> User:
        """Create a user from Google OAuth."""
        # Check if user already exists
        user = UserService.get_user_by_email(db, google_user.email)
        if user:
            return user
        
        # Create new Google user
        user = User(
            username=google_user.email,
            email=google_user.email,
            google_id=google_id,
            is_google_user=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Send welcome email
        EmailService.send_welcome_email(user.email, user.username)
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username_or_email(db: Session, username_or_email: str) -> User:
        """Get user by username or email."""
        # Try to find by username first
        user = db.query(User).filter(User.username == username_or_email).first()
        
        # If not found, try by email
        if not user:
            user = db.query(User).filter(User.email == username_or_email).first()
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, username_or_email: str, password: str) -> User:
        """Authenticate user with username/email and password."""
        user = UserService.get_user_by_username_or_email(db, username_or_email)
        if not user or not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def change_password(db: Session, user: User, current_password: str, new_password: str) -> None:
        """Change user password."""
        # Check if user is Google user
        if user.is_google_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account uses Google authentication. Password cannot be changed."
            )
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        db.commit()
    
    @staticmethod
    def set_pin(db: Session, user: User, pin: str) -> None:
        """Set user PIN."""
        # Validate PIN
        is_valid, message = validate_pin(pin)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        user.hashed_pin = get_pin_hash(pin)
        db.commit()
    
    @staticmethod
    def verify_user_pin(user: User, pin: str) -> bool:
        """Verify user PIN."""
        if not user.hashed_pin:
            return False
        
        return verify_pin(pin, user.hashed_pin)
    
    @staticmethod
    def change_pin(db: Session, user: User, current_pin: str, new_pin: str) -> None:
        """Change user PIN."""
        if not user.hashed_pin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No PIN set for this user"
            )
        
        # Verify current PIN
        if not verify_pin(current_pin, user.hashed_pin):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current PIN is incorrect"
            )
        
        # Validate new PIN
        is_valid, message = validate_pin(new_pin)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        user.hashed_pin = get_pin_hash(new_pin)
        db.commit()
    
    @staticmethod
    def remove_pin(db: Session, user: User, current_pin: str) -> None:
        """Remove user PIN."""
        if not user.hashed_pin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No PIN set for this user"
            )
        
        if not verify_pin(current_pin, user.hashed_pin):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PIN"
            )
        
        user.hashed_pin = None
        db.commit()
    
    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        """Delete user account."""
        # Delete all reset tokens for this user
        db.query(ResetToken).filter(ResetToken.user_id == user.id).delete()
        
        # Delete user
        db.delete(user)
        db.commit() 