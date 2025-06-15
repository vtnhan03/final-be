"""User schemas for request/response validation."""

from pydantic import BaseModel, EmailStr
from typing import Union


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    has_pin: bool = False
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login - accepts username or email."""
    username_or_email: str
    password: str


class ChangePasswordRequest(BaseModel):
    """Schema for changing password."""
    current_password: str
    new_password: str


class PasswordVerifyRequest(BaseModel):
    """Schema for password verification."""
    password: str


class GoogleAuthRequest(BaseModel):
    """Schema for Google authentication."""
    token: str
    userInfo: dict


class GoogleUser(BaseModel):
    """Schema for Google user data."""
    email: EmailStr
    name: str
    given_name: str
    family_name: str
    email_verified: bool 