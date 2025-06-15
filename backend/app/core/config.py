import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Starter Web App"
    VERSION: str = "1.0.0"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    def __init__(self):
        # Add production origins if in production
        if self.ENVIRONMENT == "production":
            production_origin = os.getenv("FRONTEND_URL")
            if production_origin:
                # Normalize URL - remove trailing slash and add both versions
                normalized_url = production_origin.rstrip('/')
                self.ALLOWED_ORIGINS.extend([
                    normalized_url,           # without trailing slash
                    normalized_url + '/'      # with trailing slash
                ])
            
            # Also check for specific Cloudflare URL
            cloudflare_url = os.getenv("CLOUDFLARE_WORKERS_URL")
            if cloudflare_url:
                normalized_cf_url = cloudflare_url.rstrip('/')
                self.ALLOWED_ORIGINS.extend([
                    normalized_cf_url,        # without trailing slash
                    normalized_cf_url + '/'   # with trailing slash
                ])
        
        # Remove duplicates and print for debugging
        self.ALLOWED_ORIGINS = list(set(self.ALLOWED_ORIGINS))
        print(f"🔗 CORS Allowed Origins: {self.ALLOWED_ORIGINS}")

settings = Settings()