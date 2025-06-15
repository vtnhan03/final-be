"""Google OAuth authentication utilities."""

import logging
from typing import Optional
import requests
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas import GoogleUser

logger = logging.getLogger(__name__)


async def verify_google_token(token: str) -> Optional[GoogleUser]:
    """Verify Google ID token and return user information."""
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        logger.info(f"Verifying Google token (length: {len(token)})")
        
        # Call Google's userinfo API
        url = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}"
        
        response = requests.get(url, timeout=10)
        logger.info(f"Google API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Google API error: {response.text}")
            return None
        
        user_data = response.json()
        logger.info(f"Google user data received: {user_data}")
        
        # Validate required fields
        required_fields = ["email", "name", "given_name", "family_name"]
        for field in required_fields:
            if field not in user_data:
                logger.error(f"Missing required field: {field}")
                return None
        
        # Create GoogleUser object
        google_user = GoogleUser(
            email=user_data["email"],
            name=user_data["name"],
            given_name=user_data["given_name"],
            family_name=user_data["family_name"],
            email_verified=user_data.get("verified_email", True)
        )
        
        return google_user
        
    except requests.RequestException as e:
        logger.error(f"Network error verifying Google token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error verifying Google token: {str(e)}")
        return None 