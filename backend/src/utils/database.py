"""
Database utilities for connecting to Qdrant and Neon Postgres
"""
from typing import Optional
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    neon_database_url: str
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    class Config:
        env_file = ".env"


# Initialize settings
settings = DatabaseSettings()

# Qdrant client setup
if settings.qdrant_api_key:
    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
else:
    qdrant_client = QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )

# Postgres setup
engine = create_engine(
    settings.neon_database_url,
    pool_pre_ping=True,
    echo=False  # Set to True for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()