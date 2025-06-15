#!/usr/bin/env python3
"""
Production deployment script for the backend.
Handles database migrations and other deployment tasks.
"""
import os
import sys
import subprocess

def run_command(command: str, description: str):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr.strip()}")
        return False

def check_environment():
    """Check if we're in production environment"""
    env = os.getenv("ENVIRONMENT", "development")
    if env != "production":
        print(f"⚠️  Warning: ENVIRONMENT is set to '{env}', not 'production'")
        if not sys.stdin.isatty() or os.getenv("CI", "false").lower() == "true":
            print("Skipping prompt due to non-interactive environment or CI mode")
            print("Deployment cancelled")
            sys.exit(1)
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled")
            sys.exit(1)
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable is not set")
        sys.exit(1)
    
    if "sqlite" in database_url:
        print("⚠️  Warning: Using SQLite database (development mode)")
    
    print(f"✅ Environment check passed (ENV: {env})")

def run_migrations():
    """Run Alembic migrations"""
    return run_command("alembic upgrade head", "Running database migrations")

def main():
    """Main deployment function"""
    print("🚀 Starting production deployment...")
    
    # Check environment
    check_environment()
    
    # Run migrations
    if not run_migrations():
        print("❌ Deployment failed due to migration errors")
        sys.exit(1)
    
    print("🎉 Deployment completed successfully!")
    print("The application is ready to start with: uvicorn app.main:app --host 0.0.0.0 --port $PORT")

if __name__ == "__main__":
    main()