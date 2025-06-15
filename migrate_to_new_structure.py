#!/usr/bin/env python3
"""
Migration script to transition from old project structure to new structure.
This script will help you safely migrate your existing code.
"""

import os
import shutil
import sys
from pathlib import Path


def backup_old_files():
    """Create backup of important files."""
    print("📦 Creating backup of existing files...")
    
    backup_dir = Path("backup_old_structure")
    backup_dir.mkdir(exist_ok=True)
    
    # Files to backup
    files_to_backup = [
        "main.py",
        "requirements.txt",
        ".env",
        "API_DOCUMENTATION.md",
        "environment_variables.md",
        "README.md"
    ]
    
    for file in files_to_backup:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"  ✅ Backed up {file}")
    
    # Backup app directory if it exists
    if Path("app").exists():
        if (backup_dir / "app").exists():
            shutil.rmtree(backup_dir / "app")
        shutil.copytree("app", backup_dir / "app")
        print("  ✅ Backed up app/ directory")
    
    print(f"📦 Backup completed in {backup_dir}/")


def check_new_structure():
    """Check if new structure is properly created."""
    print("\n🔍 Checking new project structure...")
    
    required_dirs = [
        "app",
        "app/api",
        "app/api/v1",
        "app/auth",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "app/services",
        "app/utils"
    ]
    
    required_files = [
        "app/__init__.py",
        "app/core/config.py",
        "app/db/database.py",
        "app/models/user.py",
        "app/models/reset_token.py",
        "app/schemas/user.py",
        "app/schemas/auth.py",
        "app/services/user_service.py",
        "app/services/email_service.py",
        "app/auth/dependencies.py",
        "app/api/v1/auth.py",
        "app/api/v1/users.py",
        "main.py"
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_dirs:
        print("❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
    
    if not missing_dirs and not missing_files:
        print("✅ All required files and directories are present!")
        return True
    
    return False


def test_imports():
    """Test if all imports work correctly."""
    print("\n🧪 Testing imports...")
    
    try:
        # Test core imports
        from app.core.config import settings
        print("  ✅ Core config import successful")
        
        # Test database imports
        from app.db import get_db, create_tables
        print("  ✅ Database imports successful")
        
        # Test model imports
        from app.models import User, ResetToken
        print("  ✅ Model imports successful")
        
        # Test schema imports
        from app.schemas import UserCreate, UserOut, Token
        print("  ✅ Schema imports successful")
        
        # Test service imports
        from app.services import UserService, EmailService
        print("  ✅ Service imports successful")
        
        # Test auth imports
        from app.auth import get_current_user
        print("  ✅ Auth imports successful")
        
        # Test API imports
        from app.api.v1.router import api_router
        print("  ✅ API router import successful")
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def show_next_steps():
    """Show next steps for the user."""
    print("\n🚀 Next Steps:")
    print("1. Review the new project structure in PROJECT_STRUCTURE.md")
    print("2. Update your .env file with required environment variables")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Test the application: python main.py")
    print("5. Check API documentation: http://localhost:8000/docs")
    print("\n📚 Documentation:")
    print("- PROJECT_STRUCTURE.md - Detailed architecture overview")
    print("- API_DOCUMENTATION.md - API endpoint documentation")
    print("- environment_variables.md - Environment setup guide")


def main():
    """Main migration function."""
    print("🔄 ChildSafe API - Project Structure Migration")
    print("=" * 50)
    
    # Step 1: Backup existing files
    backup_old_files()
    
    # Step 2: Check new structure
    structure_ok = check_new_structure()
    
    if not structure_ok:
        print("\n❌ New project structure is incomplete.")
        print("Please ensure all files have been created properly.")
        sys.exit(1)
    
    # Step 3: Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Import tests failed.")
        print("Please check for any missing dependencies or syntax errors.")
        sys.exit(1)
    
    # Step 4: Show next steps
    show_next_steps()
    
    print("\n✅ Migration completed successfully!")
    print("Your old files are safely backed up in backup_old_structure/")


if __name__ == "__main__":
    main() 