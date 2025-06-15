"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import (
    UserCreate, UserLogin, UserOut, Token, GoogleAuthRequest,
    ForgotPasswordRequest, ResetPasswordRequest, ResetPasswordWithCodeRequest, 
    MessageResponse, PasswordVerifyRequest
)
from app.services import UserService, ResetService
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.auth.google_auth import verify_google_token
from app.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user = UserService.create_user(db, user_data)
    return UserOut(id=user.id, username=user.username, has_pin=bool(user.hashed_pin))


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with username/email and password."""
    user = UserService.authenticate_user(db, user_data.username_or_email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/verify-password", response_model=MessageResponse)
async def verify_password_endpoint(
    request: PasswordVerifyRequest,
    current_user: User = Depends(get_current_user)
):
    """Verify the current user's password."""
    # Check if user is Google user
    if current_user.is_google_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account uses Google authentication. Password verification is not available."
        )
    
    # Verify password
    if not current_user.hashed_password or not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    return MessageResponse(message="Password verified successfully")


@router.post("/google", response_model=Token)
async def google_auth(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate with Google OAuth."""
    # Verify Google token
    google_user = await verify_google_token(auth_data.token)
    if not google_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    # Create or get existing user
    user = UserService.create_google_user(db, google_user)
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset with verification code."""
    message = ResetService.request_password_reset(db, request.email)
    return MessageResponse(message=message)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token (URL-based reset)."""
    message = ResetService.reset_password(db, request.token, request.new_password)
    return MessageResponse(message=message)


@router.post("/reset-password-with-code", response_model=MessageResponse)
async def reset_password_with_code(request: ResetPasswordWithCodeRequest, db: Session = Depends(get_db)):
    """Reset password using verification code (form-based reset)."""
    message = ResetService.reset_password_with_code(
        db, request.email, request.verification_code, request.new_password
    )
    return MessageResponse(message=message) 