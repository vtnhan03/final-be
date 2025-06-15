"""Health check and utility endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import HealthCheck, MessageResponse
from app.core.config import settings
from app.services.email_service import EmailService

router = APIRouter(tags=["Health & Utilities"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=settings.app_version,
        service=settings.app_name
    )


@router.post("/test-email", response_model=MessageResponse)
async def test_email():
    """Test email functionality."""
    success = EmailService.send_welcome_email(
        "test@example.com", 
        "Test User"
    )
    
    if success:
        return MessageResponse(message="Test email sent successfully")
    else:
        return MessageResponse(message="Failed to send test email") 