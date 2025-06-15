"""Common schemas used across the application."""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    message: str


class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    version: str
    service: str 