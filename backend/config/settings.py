from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Humanoid Robotics Book RAG API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Database settings
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL", "")

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))

    # Cohere settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()