"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import (
    UserOut, ChangePasswordRequest, MessageResponse,
    PinCreate, PinVerify, PinVerifyResponse, PinRemove,
    ChangePinRequest, ForgotPinRequest, ResetPinRequest, ResetPinWithCodeRequest,
    PasswordVerifyRequest
)
from app.services import UserService, ResetService
from app.auth import get_current_user
from app.utils.security import verify_password

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        has_pin=bool(current_user.hashed_pin)
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password."""
    UserService.change_password(
        db, current_user, request.current_password, request.new_password
    )
    return MessageResponse(message="Password changed successfully")


@router.delete("/me", response_model=MessageResponse)
async def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user account."""
    UserService.delete_user(db, current_user)
    return MessageResponse(message="Account deleted successfully")


# PIN Management Endpoints
@router.post("/pin", response_model=MessageResponse)
async def set_pin(
    request: PinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Set user PIN."""
    UserService.set_pin(db, current_user, request.pin)
    return MessageResponse(message="PIN set successfully")


@router.post("/pin/verify", response_model=PinVerifyResponse)
async def verify_pin(
    request: PinVerify,
    current_user: User = Depends(get_current_user)
):
    """Verify user PIN."""
    # Check if user has a PIN set
    if not current_user.hashed_pin:
        return PinVerifyResponse(
            valid=False,
            message="No PIN set for this user"
        )
    
    is_valid = UserService.verify_user_pin(current_user, request.pin)
    return PinVerifyResponse(
        valid=is_valid,
        message="PIN is valid" if is_valid else "PIN is invalid"
    )


@router.put("/pin", response_model=MessageResponse)
async def change_pin(
    request: ChangePinRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user PIN."""
    UserService.change_pin(db, current_user, request.current_pin, request.new_pin)
    return MessageResponse(message="PIN changed successfully")


@router.delete("/pin", response_model=MessageResponse)
async def remove_pin(
    request: PinRemove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove user PIN."""
    UserService.remove_pin(db, current_user, request.current_pin)
    return MessageResponse(message="PIN removed successfully")


@router.delete("/pin/force-remove", response_model=MessageResponse)
async def force_remove_pin(
    request: PasswordVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Force remove PIN using password verification (for forgotten PIN)."""
    # Check if user is Google user
    if current_user.is_google_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account uses Google authentication. Password verification is not available."
        )
    
    # Check if user has a PIN to remove
    if not current_user.hashed_pin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No PIN set for this user"
        )
    
    # Verify password
    if not current_user.hashed_password or not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Remove PIN
    current_user.hashed_pin = None
    db.commit()
    
    return MessageResponse(message="PIN removed successfully")


@router.post("/pin/forgot", response_model=MessageResponse)
async def forgot_pin(request: ForgotPinRequest, db: Session = Depends(get_db)):
    """Request PIN reset with verification code."""
    message = ResetService.request_pin_reset(db, request.email)
    return MessageResponse(message=message)


@router.post("/pin/reset", response_model=MessageResponse)
async def reset_pin(request: ResetPinRequest, db: Session = Depends(get_db)):
    """Reset PIN using token (URL-based reset)."""
    message = ResetService.reset_pin(db, request.token, request.new_pin)
    return MessageResponse(message=message)


@router.post("/pin/reset-with-code", response_model=MessageResponse)
async def reset_pin_with_code(request: ResetPinWithCodeRequest, db: Session = Depends(get_db)):
    """Reset PIN using verification code (form-based reset)."""
    message = ResetService.reset_pin_with_code(
        db, request.email, request.verification_code, request.new_pin
    )
    return MessageResponse(message=message) 