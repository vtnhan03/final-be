#!/usr/bin/env python3
"""
Manual database migration script.
Run this if you need to update the database schema manually.
"""

import logging
import sys
from app.db.migrations import run_migrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run database migrations manually."""
    print("🔄 ChildSafe Database Migration")
    print("=" * 40)
    
    try:
        run_migrations()
        print("\n✅ Database migration completed successfully!")
        print("Your database is now up to date with the latest schema.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("Please check your database connection and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main() 