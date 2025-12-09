"""
Chat service for managing conversations and chat sessions
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import logging
import uuid
from datetime import datetime, timedelta

from backend.src.models.chat_models import ChatSession, ChatMessage
from backend.src.utils.logger import chat_logger


class ChatService:
    """Service for managing chat sessions and messages."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_session(self, user_id: str = None) -> ChatSession:
        """Create a new chat session."""
        chat_logger.info("Creating new chat session")

        session_token = f"sess_{uuid.uuid4().hex[:16]}"
        expires_at = datetime.utcnow() + timedelta(days=7)  # Session expires in 7 days

        session = ChatSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        chat_logger.info(f"Chat session created: {session.id}")
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID."""
        chat_logger.info(f"Retrieving chat session: {session_id}")
        return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()

    def get_session_by_token(self, session_token: str) -> Optional[ChatSession]:
        """Get a chat session by session token."""
        chat_logger.info(f"Retrieving chat session by token: {session_token}")
        return self.db.query(ChatSession).filter(ChatSession.session_token == session_token).first()

    def create_message(self, session_id: str, role: str, content: str,
                       retrieved_context: List[Dict] = None, model_used: str = None,
                       tokens_used: int = 0, relevance_score: float = None) -> ChatMessage:
        """Create a new chat message."""
        chat_logger.info(f"Creating message for session: {session_id}, role: {role}")

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            retrieved_context=retrieved_context,
            model_used=model_used,
            tokens_used=tokens_used,
            relevance_score=relevance_score
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        chat_logger.info(f"Message created: {message.id}")
        return message

    def get_messages(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get messages for a session, ordered by creation time."""
        chat_logger.info(f"Retrieving messages for session: {session_id}")

        return self.db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.created_at.asc())\
            .limit(limit)\
            .all()

    def get_recent_messages(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Get the most recent messages for a session."""
        chat_logger.info(f"Retrieving recent messages for session: {session_id}")

        return self.db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(desc(ChatMessage.created_at))\
            .limit(limit)\
            .all()

    def update_session_title(self, session_id: str, title: str) -> Optional[ChatSession]:
        """Update the title of a chat session."""
        chat_logger.info(f"Updating session title for: {session_id}")

        session = self.get_session(session_id)
        if session:
            session.title = title
            self.db.commit()
            self.db.refresh(session)

        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session and all its messages."""
        chat_logger.info(f"Deleting chat session: {session_id}")

        session = self.get_session(session_id)
        if session:
            # Delete all messages in the session first
            self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
            # Then delete the session
            self.db.delete(session)
            self.db.commit()
            return True

        return False

    def clear_expired_sessions(self) -> int:
        """Remove expired chat sessions."""
        chat_logger.info("Clearing expired chat sessions")

        expired_count = self.db.query(ChatSession)\
            .filter(ChatSession.expires_at < datetime.utcnow())\
            .delete()

        self.db.commit()
        chat_logger.info(f"Cleared {expired_count} expired sessions")

        return expired_count