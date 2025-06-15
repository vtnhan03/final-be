"""Reset token database model."""

from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base


class ResetToken(Base):
    """Reset token model for password and PIN reset functionality."""
    
    __tablename__ = "reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String(255), unique=True, index=True)
    token_type = Column(String(20))  # 'password' or 'pin'
    expires_at = Column(String(50))  # ISO format datetime string
    used = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<ResetToken(id={self.id}, user_id={self.user_id}, type='{self.token_type}', used={self.used})>" 