from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User

app = FastAPI(title="Starter Web App API", version="1.0.0")

class CORSDebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        if origin:
            print(f"🌐 CORS Request from origin: '{origin}'")
            print(f"🔍 Allowed origins: {settings.ALLOWED_ORIGINS}")
            if origin in settings.ALLOWED_ORIGINS:
                print(f"✅ Origin '{origin}' is allowed")
            else:
                print(f"❌ Origin '{origin}' is NOT in allowed list")
        
        response = await call_next(request)
        return response

# Add CORS debugging middleware first
app.add_middleware(CORSDebugMiddleware)

# Then add the actual CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/hello")
def api_hello():
    return {"message": "Hello from API"}

@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users