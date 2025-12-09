"""
Main FastAPI application for the Humanoid Robotics Book RAG API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

from backend.src.api.v1.rag import router as rag_router
from backend.src.api.v1.content import router as content_router
from backend.src.api.v1.chat import router as chat_router
from backend.src.config import settings
from backend.src.utils.logger import app_logger


# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug
)

# Add CORS middleware
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routers
app.include_router(rag_router, prefix=settings.api_v1_str)
app.include_router(content_router, prefix=settings.api_v1_str)
app.include_router(chat_router, prefix=settings.api_v1_str)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    app_logger.info("Health check endpoint called")
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.now()}


@app.get("/")
async def root():
    """Root endpoint."""
    app_logger.info("Root endpoint called")
    return {"message": "Welcome to the Humanoid Robotics Book RAG API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)