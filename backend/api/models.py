from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SourceCitation(BaseModel):
    section_id: str
    title: str
    location: str

class QueryRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    query_type: Optional[str] = "full_book"  # Either "full_book" or "selected_text_only"

class QueryResponse(BaseModel):
    answer: str
    source_citations: List[SourceCitation]
    session_id: str

class ChatSession(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    metadata: dict = {}

class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    source_citations: List[SourceCitation] = []
    query_context: Optional[dict] = None