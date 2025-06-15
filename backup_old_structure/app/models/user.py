"""User database model."""

from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base


class User(Base):
    """User model for authentication and account management."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    hashed_pin = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    google_id = Column(String(50), unique=True, index=True, nullable=True)
    is_google_user = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>" 