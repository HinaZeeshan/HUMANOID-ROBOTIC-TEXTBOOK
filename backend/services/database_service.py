import json
from datetime import datetime
import uuid
from typing import Optional, List

# Simple database service using in-memory storage for testing
# In production, replace with proper database implementation

# Global storage for in-memory database
_global_sessions = {}
_global_messages = {}

class DatabaseService:
    def __init__(self):
        # In-memory storage for testing (using global variables for persistence)
        self.sessions = _global_sessions
        self.messages = _global_messages

    def get_session(self, session_id: str):
        """Get a chat session by ID"""
        return self.sessions.get(session_id)

    def create_session(self, user_id: Optional[str] = None, metadata: dict = {}):
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        session_data = {
            "id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "metadata": metadata
        }
        self.sessions[session_id] = session_data
        self.messages[session_id] = []
        return session_data

    def get_messages(self, session_id: str):
        """Get all messages for a session"""
        return self.messages.get(session_id, [])

    def create_message(self, session_id: str, role: str, content: str, source_citations: List[dict] = [], query_context: dict = {}):
        """Create a new chat message"""
        message_id = str(uuid.uuid4())
        message_data = {
            "id": message_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "source_citations": source_citations,
            "query_context": query_context
        }

        if session_id not in self.messages:
            self.messages[session_id] = []

        self.messages[session_id].append(message_data)
        return message_data