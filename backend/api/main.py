from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from ..config.settings import settings

# Create FastAPI app with configuration from settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routes with v1 prefix
app.include_router(router, prefix=f"{settings.API_V1_STR}")

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API for Humanoid Robotics Book"}