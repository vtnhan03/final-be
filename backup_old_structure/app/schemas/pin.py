"""PIN management schemas."""

from pydantic import BaseModel, EmailStr


class PinCreate(BaseModel):
    """Schema for creating a PIN."""
    pin: str


class PinVerify(BaseModel):
    """Schema for PIN verification."""
    pin: str


class PinVerifyResponse(BaseModel):
    """Schema for PIN verification response."""
    valid: bool
    message: str


class PinRemove(BaseModel):
    """Schema for PIN removal."""
    current_pin: str


class ChangePinRequest(BaseModel):
    """Schema for changing PIN."""
    current_pin: str
    new_pin: str


class ForgotPinRequest(BaseModel):
    """Schema for forgot PIN request."""
    email: EmailStr


class ResetPinRequest(BaseModel):
    """Schema for PIN reset."""
    token: str
    new_pin: str 