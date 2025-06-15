"""JWT token utilities."""

import datetime
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.datetime.utcnow() + datetime.timedelta(
    #         minutes=settings.access_token_expire_minutes
    #     )
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None 