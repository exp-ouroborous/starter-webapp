from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

def get_engine():
    """Create database engine with appropriate configuration"""
    # Configure engine based on database type
    if "sqlite" in settings.DATABASE_URL:
        # SQLite configuration for development
        return create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
    elif "postgresql" in settings.DATABASE_URL:
        # PostgreSQL configuration for production
        # Convert postgresql:// to postgresql+psycopg:// for psycopg3 driver
        database_url = settings.DATABASE_URL
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        return create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20
        )
    else:
        # Fallback configuration
        return create_engine(settings.DATABASE_URL)

# Create engine lazily
engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)