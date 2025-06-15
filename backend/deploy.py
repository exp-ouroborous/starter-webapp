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
        # In automated deployment, don't prompt for input
        if os.getenv("CI") or os.getenv("RENDER"):
            print("Running in automated environment, continuing...")
        else:
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
    elif "postgresql" in database_url:
        print("✅ Using PostgreSQL database (production mode)")
        print("✅ Database driver check skipped (validated during migration)")
    
    print(f"✅ Environment check passed (ENV: {env})")

def run_migrations():
    """Run Alembic migrations"""
    print("🔄 Running database migrations...")
    try:
        result = subprocess.run("alembic upgrade head", shell=True, check=True, capture_output=True, text=True)
        print("✅ Database migrations completed successfully")
        if result.stdout:
            print(f"Migration output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Database migrations failed")
        print(f"Migration error: {e}")
        if e.stdout:
            print(f"Migration stdout: {e.stdout.strip()}")
        if e.stderr:
            print(f"Migration stderr: {e.stderr.strip()}")
        print("Note: This may be due to database connectivity or migration file issues")
        print("Check that DATABASE_URL is correct and database is accessible")
        return False

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