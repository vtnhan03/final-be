"""Authentication schemas."""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str


class ResetPasswordWithCodeRequest(BaseModel):
    """Schema for password reset using verification code."""
    email: EmailStr
    verification_code: str
    new_password: str 