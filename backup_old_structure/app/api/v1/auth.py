"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    UserCreate, UserLogin, UserOut, Token, GoogleAuthRequest,
    ForgotPasswordRequest, ResetPasswordRequest, MessageResponse
)
from app.services import UserService, ResetService
from app.utils.jwt import create_access_token
from app.auth.google_auth import verify_google_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    user = UserService.create_user(db, user_data)
    return UserOut(id=user.id, username=user.username, has_pin=bool(user.hashed_pin))


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with username and password."""
    user = UserService.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


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
    """Request password reset."""
    message = ResetService.request_password_reset(db, request.email)
    return MessageResponse(message=message)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token."""
    message = ResetService.reset_password(db, request.token, request.new_password)
    return MessageResponse(message=message) 