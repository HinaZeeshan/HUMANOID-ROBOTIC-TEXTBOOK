"""
Chat API endpoints for the Humanoid Robotics Book + RAG Chatbot project
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from backend.src.utils.database import get_db
from backend.src.services.chat_service import ChatService


router = APIRouter()


class ChatSessionCreateRequest(BaseModel):
    user_id: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: str
    session_token: str
    user_id: Optional[str]
    title: Optional[str]
    created_at: str


class ChatMessageRequest(BaseModel):
    session_token: str
    content: str


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: str


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    request: ChatSessionCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    try:
        chat_service = ChatService(db)
        session = chat_service.create_session(user_id=request.user_id)

        return ChatSessionResponse(
            id=str(session.id),
            session_token=session.session_token,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat session: {str(e)}")


@router.get("/sessions/{session_token}/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_token: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a session."""
    try:
        chat_service = ChatService(db)

        # Get the session first to verify it exists
        session = chat_service.get_session_by_token(session_token)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        messages = chat_service.get_messages(session.id, limit)

        return ChatHistoryResponse(
            messages=[
                ChatMessageResponse(
                    id=str(msg.id),
                    session_id=str(msg.session_id),
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at.isoformat()
                )
                for msg in messages
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")


@router.delete("/sessions/{session_token}")
async def delete_chat_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Delete a chat session."""
    try:
        chat_service = ChatService(db)

        # Get the session first to verify it exists
        session = chat_service.get_session_by_token(session_token)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        success = chat_service.delete_session(str(session.id))

        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat session: {str(e)}")


@router.get("/health")
async def chat_health():
    """Health check for the chat service."""
    return {"status": "Chat service is healthy", "timestamp": __import__('datetime').datetime.now()}