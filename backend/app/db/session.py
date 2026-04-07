"""
app/db/session.py
SQLAlchemy engine, session factory, and FastAPI dependency for DB access.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,        # Check connection health before use
    pool_size=10,              # Connection pool size
    max_overflow=20,           # Extra connections allowed above pool_size
    echo=settings.DEBUG,       # Log SQL queries in debug mode
)

# Session factory — each request gets its own session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    FastAPI dependency that provides a DB session per request.
    Session is automatically closed after the request completes.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()