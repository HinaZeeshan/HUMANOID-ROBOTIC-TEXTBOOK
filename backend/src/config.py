"""
Configuration management for the Humanoid Robotics Book + RAG Chatbot project
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from typing import Dict, Any
import os


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    # Project settings
    project_name: str = "Humanoid Robotics Book RAG API"
    api_v1_str: str = "/api/v1"
    debug: bool = False

    # CORS settings
    backend_cors_origins: List[str] = ["*"]

    # Database settings
    neon_database_url: str
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # Cohere settings (for embeddings and response generation)
    cohere_api_key: str

    # Application settings
    default_model: str = "command-r-plus"  # Cohere model for response generation
    embedding_model: str = "embed-english-v3.0"  # Cohere embedding model

    # RAG settings
    max_chunks_per_query: int = 5
    similarity_threshold: float = 0.7

    # Content settings
    max_word_count_per_chunk: int = 1000
    min_chunk_overlap: int = 100

    # Rate limiting (if needed)
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # in seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single instance of settings
settings = Settings()


def get_settings() -> Settings:
    """Get the application settings."""
    return settings