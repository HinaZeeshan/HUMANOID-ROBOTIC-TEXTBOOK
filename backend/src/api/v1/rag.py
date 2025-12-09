"""
RAG API endpoints for the Humanoid Robotics Book + RAG Chatbot project
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any

from backend.src.utils.database import get_db
from backend.src.services.rag_service import RAGService


router = APIRouter()


class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The query text to search for")
    context_filter: Optional[str] = Field(None, pattern=r"^(module-[1-5]|chapter-.+)?$", description="Context filter for specific module (e.g., 'module-1')")
    selected_text_only: Optional[bool] = Field(False, description="Whether to use only the selected text for context")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Specific text to use as context when selected_text_only is true")
    max_chunks: Optional[int] = Field(5, ge=1, le=20, description="Maximum number of content chunks to retrieve (1-20)")
    cross_module: Optional[bool] = Field(False, description="Whether to perform cross-module search")

    @model_validator(mode='after')
    def validate_selected_text_requirement(self):
        if self.selected_text_only and not self.selected_text:
            raise ValueError("selected_text must be provided when selected_text_only is True")
        return self


class RAGSource(BaseModel):
    title: str
    module: str
    chapter: str
    relevance_score: float


class RAGQueryResponse(BaseModel):
    response: str
    sources: List[RAGSource]
    query_time_ms: int


@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest, db: Session = Depends(get_db)):
    """Query the RAG system and get a response based on book content."""
    try:
        rag_service = RAGService(db)

        if request.cross_module:
            # Handle cross-module queries that span multiple textbook modules
            result = rag_service.query(
                query=request.query,
                context_filter=request.context_filter,
                selected_text_only=request.selected_text_only,
                selected_text=request.selected_text,
                max_chunks=request.max_chunks,
                cross_module=True
            )

            return RAGQueryResponse(
                response=result["response"],
                sources=result["sources"],
                query_time_ms=result["query_time_ms"]
            )
        else:
            # Handle regular queries with context filtering
            result = rag_service.query(
                query=request.query,
                context_filter=request.context_filter,
                selected_text_only=request.selected_text_only,
                selected_text=request.selected_text,
                max_chunks=request.max_chunks,
                cross_module=False
            )

            return RAGQueryResponse(
                response=result["response"],
                sources=result["sources"],
                query_time_ms=result["query_time_ms"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def rag_health():
    """Health check for the RAG service."""
    return {"status": "RAG service is healthy", "timestamp": __import__('datetime').datetime.now()}