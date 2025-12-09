"""
Book content models for the Humanoid Robotics Book + RAG Chatbot project
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from backend.src.utils.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)  # Sequential order (1-4)
    word_count = Column(Integer, default=0)
    estimated_time = Column(Integer)  # in minutes
    learning_objectives = Column(JSON)  # List of learning objectives
    prerequisites = Column(JSON)  # List of prerequisites
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text)  # Markdown content
    order = Column(Integer, nullable=False)  # Order within the module
    word_count = Column(Integer, default=0)
    estimated_time = Column(Integer)  # in minutes
    section_headers = Column(JSON)  # List of section headers in the chapter
    diagram_count = Column(Integer, default=0)
    example_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ContentBlock(Base):
    __tablename__ = "content_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    type = Column(String(50), nullable=False)  # text, code, diagram, example, exercise
    content = Column(Text, nullable=False)  # The actual content (markdown or code)
    order = Column(Integer, nullable=False)  # Order within the chapter
    title = Column(String(200))  # Optional title for the content block
    language = Column(String(50))  # For code blocks (python, cpp, bash, etc.)
    caption = Column(Text)  # Caption for diagrams/examples
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Citation(Base):
    __tablename__ = "citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"))
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"))
    citation_text = Column(Text, nullable=False)  # Full APA-formatted citation
    url = Column(String(500))  # URL if available
    accessed_date = Column(DateTime)  # Date when the source was accessed
    type = Column(String(50))  # book, article, documentation, website
    author = Column(String(200))  # Author of the source
    title = Column(String(500))  # Title of the source
    publication_info = Column(String(500))  # Publication details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())