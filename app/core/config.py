"""
Core configuration settings for ChildSafe application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App Info
    app_name: str = "ChildSafe API"
    app_version: str = "1.0.0"
    description: str = "Secure content filtering service"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secure-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "password")
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: str = os.getenv("MYSQL_PORT", "3306")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "childsafe_db")
    
    # Google OAuth
    google_client_id: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    
    # Email Service (Resend)
    resend_api_key: Optional[str] = os.getenv("RESEND_API_KEY")
    from_email: str = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    to_email: str = os.getenv("TO_EMAIL", "delivered@resend.dev")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # CORS
    allowed_origins: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    @property
    def database_url(self) -> str:
        """Construct database URL."""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset=utf8mb4"
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 