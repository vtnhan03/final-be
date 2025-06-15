"""Security utilities for password hashing and validation."""

import secrets
import random
from passlib.context import CryptContext

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_pin_hash(pin: str) -> str:
    """Hash a PIN."""
    return pwd_context.hash(pin)


def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Verify a PIN against its hash."""
    if not hashed_pin:
        return False
    return pwd_context.verify(plain_pin, hashed_pin)


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"


def validate_pin(pin: str) -> tuple[bool, str]:
    """Validate PIN format."""
    if not pin.isdigit():
        return False, "PIN must contain only digits"
    if len(pin) < 4 or len(pin) > 6:
        return False, "PIN must be 4-6 digits"
    return True, "PIN is valid"


def generate_reset_token() -> str:
    """Generate a secure random token for password/PIN reset."""
    return secrets.token_urlsafe(32)


def generate_verification_code() -> str:
    """Generate a 6-digit verification code."""
    return f"{random.randint(100000, 999999):06d}" 