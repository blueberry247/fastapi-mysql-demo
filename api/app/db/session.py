from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# SQLAlchemy engine: one per process
engine = create_engine(
    settings.sqlalchemy_database_uri,
    pool_pre_ping=True,
)

# Session factory: used to create DB sessions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a DB session
    and makes sure it is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

