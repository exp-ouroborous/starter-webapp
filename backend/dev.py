#!/usr/bin/env python3
"""
Development helper script for the backend.
Provides common development tasks like running the server, database operations, etc.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def ensure_venv():
    """Ensure virtual environment exists and is activated"""
    if not os.path.exists("venv"):
        print("🔄 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    
    # Check if we're in venv
    if "venv" not in sys.prefix:
        venv_python = "venv\\Scripts\\python.exe" if sys.platform == "win32" else "venv/bin/python"
        print(f"⚠️  Please activate the virtual environment first:")
        print(f"   source venv/bin/activate  # Linux/Mac")
        print(f"   venv\\Scripts\\activate     # Windows")
        print(f"   Or run: {venv_python} dev.py <command>")
        return False
    return True

def setup():
    """Set up the development environment"""
    print("🔧 Setting up development environment...")
    
    if not ensure_venv():
        return
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return
    
    # Initialize database
    if not os.path.exists("app.db"):
        run_command("alembic upgrade head", "Initializing database")
    
    # Create .env if it doesn't exist
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            run_command("cp .env.example .env", "Creating .env file from template")
        else:
            print("⚠️  .env.example not found, please create .env manually")
    
    print("✅ Development environment setup complete!")
    print("🚀 Run 'python dev.py server' to start the development server")

def server():
    """Start the development server"""
    print("🚀 Starting development server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔄 Hot reload is enabled - server will restart on code changes")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            "uvicorn", "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

def test():
    """Run tests"""
    if os.path.exists("tests"):
        run_command("python -m pytest tests/ -v", "Running tests")
    else:
        print("⚠️  No tests directory found. Consider adding tests!")

def db_reset():
    """Reset the database"""
    print("⚠️  This will delete all data in the database!")
    confirm = input("Are you sure? (y/N): ").lower()
    if confirm == 'y':
        if os.path.exists("app.db"):
            os.remove("app.db")
            print("🗑️  Database file removed")
        run_command("alembic upgrade head", "Recreating database")
    else:
        print("❌ Database reset cancelled")

def db_migrate(message=None):
    """Create a new database migration"""
    if not message:
        message = input("Enter migration message: ").strip()
        if not message:
            message = "Auto-generated migration"
    
    run_command(f'alembic revision --autogenerate -m "{message}"', f"Creating migration: {message}")

def db_upgrade():
    """Apply database migrations"""
    run_command("alembic upgrade head", "Applying database migrations")

def lint():
    """Run linting checks"""
    print("🔍 Running linting checks...")
    commands = [
        ("python -m flake8 app/ --max-line-length=88 --extend-ignore=E203,W503", "Flake8 linting"),
        ("python -m black app/ --check", "Black formatting check"),
        ("python -m isort app/ --check-only", "Import sorting check"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print("💡 Run 'python dev.py format' to fix formatting issues")
            break

def format_code():
    """Format code automatically"""
    print("🎨 Formatting code...")
    commands = [
        ("python -m black app/", "Black formatting"),
        ("python -m isort app/", "Import sorting"),
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)

def clean():
    """Clean up development files"""
    print("🧹 Cleaning up...")
    patterns = ["__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".coverage"]
    
    for pattern in patterns:
        if sys.platform == "win32":
            run_command(f"powershell -Command \"Get-ChildItem -Recurse -Name '{pattern}' | Remove-Item -Recurse -Force\"", f"Removing {pattern}")
        else:
            run_command(f"find . -name '{pattern}' -exec rm -rf {{}} + 2>/dev/null || true", f"Removing {pattern}")

def help_text():
    """Show help information"""
    print("""
🛠️  Backend Development Helper

Available commands:
  setup     - Set up the development environment
  server    - Start the development server with hot reload
  test      - Run tests
  db-reset  - Reset the database (WARNING: deletes all data)
  db-migrate [message] - Create a new database migration
  db-upgrade - Apply database migrations
  lint      - Run linting checks
  format    - Format code automatically
  clean     - Clean up development files
  help      - Show this help message

Examples:
  python dev.py setup
  python dev.py server
  python dev.py db-migrate "add user table"
  python dev.py lint
""")

def main():
    if len(sys.argv) < 2:
        help_text()
        return
    
    command = sys.argv[1].lower().replace('-', '_')
    
    commands = {
        'setup': setup,
        'server': server,
        'test': test,
        'db_reset': db_reset,
        'db_migrate': lambda: db_migrate(sys.argv[2] if len(sys.argv) > 2 else None),
        'db_upgrade': db_upgrade,
        'lint': lint,
        'format': format_code,
        'clean': clean,
        'help': help_text,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {sys.argv[1]}")
        help_text()

if __name__ == "__main__":
    main()