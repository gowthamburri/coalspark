"""
setup_verify.py - Verify CoalSpark Restaurant backend setup

Run this script to check if everything is configured correctly.
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🔥 CoalSpark Restaurant - Backend Setup Verification")
print("=" * 70)
print()

# Change to backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

errors = []
warnings = []
success = []

def check_item(condition, success_msg, error_msg, warning=False):
    """Helper to check conditions and track results."""
    if condition:
        success.append(success_msg)
        print(f"✅ {success_msg}")
    else:
        msg = f"{error_msg}"
        if warning:
            warnings.append(msg)
            print(f"⚠️  {msg}")
        else:
            errors.append(msg)
            print(f"❌ {msg}")

# 1. Check Python version
print("\n📌 Checking Python version...")
check_item(
    sys.version_info >= (3, 9),
    f"Python {sys.version_info.major}.{sys.version_info.minor} installed",
    f"Python 3.9+ required, found {sys.version_info.major}.{sys.version_info.minor}",
)

# 2. Check virtual environment
print("\n📌 Checking virtual environment...")
in_venv = sys.prefix != sys.base_prefix or 'VIRTUAL_ENV' in os.environ
check_item(
    in_venv,
    "Virtual environment is active",
    "Virtual environment not activated! Run: venv\\Scripts\\activate",
)

# 3. Check required packages
print("\n📌 Checking required packages...")
required_packages = [
    'fastapi', 'uvicorn', 'sqlalchemy', 'pydantic',
    'python-jose', 'passlib', 'alembic', 'python-dotenv'
]

for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        check_item(True, f"{package} installed", "")
    except ImportError:
        check_item(False, "", f"{package} not installed! Run: pip install {package}")

# 4. Check .env file
print("\n📌 Checking .env configuration...")
env_file = backend_dir / '.env'
check_item(
    env_file.exists(),
    ".env file exists",
    ".env file not found! Create one with DATABASE_URL and SECRET_KEY",
)

if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    
    check_item(
        database_url is not None,
        "DATABASE_URL is set",
        "DATABASE_URL not set in .env!",
    )
    
    check_item(
        secret_key is not None and len(secret_key) >= 32,
        "SECRET_KEY is set (min 32 chars)",
        "SECRET_KEY too short or not set! Generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"",
    )
    
    # Check if using default secret key
    if secret_key and 'your-super-secret-key' in secret_key:
        check_item(False, "", "Using default SECRET_KEY! Generate a unique one for security.", warning=True)

# 5. Check alembic configuration
print("\n📌 Checking Alembic migration setup...")
alembic_ini = backend_dir / 'alembic.ini'
check_item(
    alembic_ini.exists(),
    "alembic.ini exists",
    "alembic.ini not found!",
)

alembic_env = backend_dir / 'alembic' / 'env.py'
check_item(
    alembic_env.exists(),
    "alembic/env.py exists",
    "alembic/env.py not found!",
)

# 6. Check app structure
print("\n📌 Checking application structure...")
app_dirs = [
    'app',
    'app/api',
    'app/api/routes',
    'app/core',
    'app/db',
    'app/models',
    'app/repositories',
    'app/schemas',
    'app/services',
    'app/utils',
]

for dir_path in app_dirs:
    check_item(
        (backend_dir / dir_path).exists(),
        f"Directory {dir_path}/ exists",
        f"Directory {dir_path}/ missing!",
    )

# 7. Check critical files
print("\n📌 Checking critical files...")
critical_files = [
    'main.py',
    'app/__init__.py',
    'app/models/__init__.py',
    'app/repositories/__init__.py',
    'app/services/__init__.py',
]

for file in critical_files:
    check_item(
        (backend_dir / file).exists(),
        f"File {file} exists",
        f"File {file} missing!",
    )

# 8. Try importing app modules
print("\n📌 Testing module imports...")
try:
    from app.db.session import Base, engine, get_db
    check_item(True, "Database modules imported", "")
except Exception as e:
    check_item(False, "", f"Database import failed: {str(e)}")

try:
    from app.models import User, Restaurant, MenuItem, Order, OrderItem
    check_item(True, "Models imported successfully", "")
except Exception as e:
    check_item(False, "", f"Model import failed: {str(e)}")

try:
    from app.repositories import UserRepository, MenuRepository, OrderRepository
    check_item(True, "Repositories imported successfully", "")
except Exception as e:
    check_item(False, "", f"Repository import failed: {str(e)}")

# 9. Check database
print("\n📌 Checking database status...")
database_url = os.getenv('DATABASE_URL', '')
if database_url:
    if database_url.startswith('sqlite'):
        db_file = backend_dir / database_url.split('/')[-1]
        if db_file.exists():
            check_item(True, f"SQLite database exists ({db_file.name})", "")
        else:
            check_item(False, "", "Database file not found. Run: alembic upgrade head", warning=True)
    elif database_url.startswith('postgresql'):
        check_item(True, "PostgreSQL URL configured", "", warning=True)
        print("   ℹ️  Make sure PostgreSQL server is running and database exists")
else:
    check_item(False, "", "DATABASE_URL not configured!")

# 10. Check uploads directory
print("\n📌 Checking uploads directory...")
uploads_dir = backend_dir / 'uploads'
check_item(
    uploads_dir.exists(),
    "Uploads directory exists",
    "Uploads directory missing! Creating it...",
)

if not uploads_dir.exists():
    uploads_dir.mkdir(exist_ok=True)
    print(f"   ✅ Created {uploads_dir}/")

# Summary
print("\n" + "=" * 70)
print("📊 VERIFICATION SUMMARY")
print("=" * 70)
print(f"✅ Success: {len(success)}")
print(f"⚠️  Warnings: {len(warnings)}")
print(f"❌ Errors: {len(errors)}")
print()

if errors:
    print("🔴 CRITICAL ISSUES FOUND:")
    for error in errors:
        print(f"   • {error}")
    print()
    print("Please fix these issues before running the application.")
    print()
    sys.exit(1)
elif warnings:
    print("🟡 WARNINGS (recommended to fix):")
    for warning in warnings:
        print(f"   • {warning}")
    print()
    print("Application can run but fixing warnings is recommended.")
    print()
else:
    print("🎉 ALL CHECKS PASSED!")
    print()
    print("Your backend is ready to run!")
    print()
    print("Next steps:")
    print("1. Run: alembic upgrade head")
    print("2. Run: uvicorn main:app --reload")
    print("3. Open: http://localhost:8000/docs")
    print()

print("=" * 70)
