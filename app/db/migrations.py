"""Database migrations for schema updates."""

import logging
from sqlalchemy import text
from app.db.database import engine

logger = logging.getLogger(__name__)


def run_migrations():
    """Run all pending database migrations."""
    logger.info("Running database migrations...")
    
    try:
        with engine.connect() as connection:
            # Migration 1: Add verification_code column to reset_tokens table
            add_verification_code_column(connection)
            
        logger.info("All migrations completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


def add_verification_code_column(connection):
    """Add verification_code column to reset_tokens table if it doesn't exist."""
    try:
        # Check if column already exists
        result = connection.execute(text("""
            SELECT COUNT(*) as count 
            FROM information_schema.columns 
            WHERE table_name = 'reset_tokens' 
            AND column_name = 'verification_code'
            AND table_schema = DATABASE()
        """))
        
        column_exists = result.fetchone()[0] > 0
        
        if not column_exists:
            logger.info("Adding verification_code column to reset_tokens table...")
            connection.execute(text("""
                ALTER TABLE reset_tokens 
                ADD COLUMN verification_code VARCHAR(10) NULL
            """))
            connection.commit()
            logger.info("✅ verification_code column added successfully!")
        else:
            logger.info("✅ verification_code column already exists, skipping migration")
            
    except Exception as e:
        logger.error(f"Failed to add verification_code column: {str(e)}")
        raise 