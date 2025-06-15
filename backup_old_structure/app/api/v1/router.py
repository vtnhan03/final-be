"""Main API router for version 1."""

from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .health import router as health_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(health_router) 