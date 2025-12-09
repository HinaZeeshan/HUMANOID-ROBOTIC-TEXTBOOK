"""
RAG (Retrieval-Augmented Generation) models for the Humanoid Robotics Book + RAG Chatbot project
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from backend.src.utils.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(String, nullable=False)  # Reference to the source document (chapter ID)
    content = Column(Text, nullable=False)  # The text content of the chunk
    chunk_index = Column(Integer, nullable=False)  # Position of this chunk in the document
    # Note: embeddings are stored in Qdrant, not in Postgres
    metadata = Column(JSON)  # Additional metadata (source, section, etc.)
    token_count = Column(Integer, default=0)  # Number of tokens in the chunk
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RetrievalResult(Base):
    __tablename__ = "retrieval_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(Text, nullable=False)  # Original query
    retrieved_chunks = Column(JSON)  # IDs of retrieved document chunks
    relevance_scores = Column(JSON)  # Relevance scores for each chunk (JSON array of floats)
    search_method = Column(String(50))  # Method used for retrieval (semantic, keyword, hybrid)
    latency_ms = Column(Integer)  # Time taken for retrieval in milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String)  # User identifier if authenticated
    session_token = Column(String, unique=True, nullable=False)  # Anonymous session identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True))  # Session expiration timestamp
    title = Column(String(200))  # Auto-generated title based on first query


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)  # The message content
    retrieved_context = Column(JSON)  # Context chunks retrieved for this message
    model_used = Column(String(100))  # LLM model used for generation
    tokens_used = Column(Integer, default=0)  # Number of tokens in the response
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    relevance_score = Column(Float)  # Relevance score of the response (0-1)