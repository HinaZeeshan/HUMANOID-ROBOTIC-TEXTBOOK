"""
Content service for managing book content (modules, chapters, etc.)
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
import logging

from backend.src.models.book_content import Module, Chapter, ContentBlock, Citation
from backend.src.utils.logger import content_logger


class ContentService:
    """Service for managing book content (modules, chapters, content blocks, citations)."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_module(self, title: str, slug: str, description: str = None, order: int = None,
                      learning_objectives: List[str] = None, prerequisites: List[str] = None) -> Module:
        """Create a new module."""
        content_logger.info(f"Creating module: {title}")

        module = Module(
            title=title,
            slug=slug,
            description=description,
            order=order,
            learning_objectives=learning_objectives or [],
            prerequisites=prerequisites or []
        )

        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)

        content_logger.info(f"Module created successfully: {module.id}")
        return module

    def get_module(self, module_id: str) -> Optional[Module]:
        """Get a module by ID."""
        content_logger.info(f"Retrieving module: {module_id}")
        return self.db.query(Module).filter(Module.id == module_id).first()

    def get_module_by_slug(self, slug: str) -> Optional[Module]:
        """Get a module by slug."""
        content_logger.info(f"Retrieving module by slug: {slug}")
        return self.db.query(Module).filter(Module.slug == slug).first()

    def list_modules(self) -> List[Module]:
        """List all modules ordered by their sequence."""
        content_logger.info("Retrieving all modules")
        return self.db.query(Module).order_by(Module.order).all()

    def update_module(self, module_id: str, **kwargs) -> Optional[Module]:
        """Update a module."""
        content_logger.info(f"Updating module: {module_id}")
        module = self.get_module(module_id)
        if module:
            for key, value in kwargs.items():
                setattr(module, key, value)
            self.db.commit()
            self.db.refresh(module)
        return module

    def delete_module(self, module_id: str) -> bool:
        """Delete a module."""
        content_logger.info(f"Deleting module: {module_id}")
        module = self.get_module(module_id)
        if module:
            self.db.delete(module)
            self.db.commit()
            return True
        return False

    def create_chapter(self, module_id: str, title: str, slug: str, content: str = None,
                       order: int = None, section_headers: List[str] = None) -> Chapter:
        """Create a new chapter."""
        content_logger.info(f"Creating chapter: {title} in module: {module_id}")

        chapter = Chapter(
            module_id=module_id,
            title=title,
            slug=slug,
            content=content,
            order=order,
            section_headers=section_headers or []
        )

        self.db.add(chapter)
        self.db.commit()
        self.db.refresh(chapter)

        content_logger.info(f"Chapter created successfully: {chapter.id}")
        return chapter

    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """Get a chapter by ID."""
        content_logger.info(f"Retrieving chapter: {chapter_id}")
        return self.db.query(Chapter).filter(Chapter.id == chapter_id).first()

    def get_chapter_by_slug(self, slug: str) -> Optional[Chapter]:
        """Get a chapter by slug."""
        content_logger.info(f"Retrieving chapter by slug: {slug}")
        return self.db.query(Chapter).filter(Chapter.slug == slug).first()

    def list_chapters_by_module(self, module_id: str) -> List[Chapter]:
        """List all chapters in a module ordered by their sequence."""
        content_logger.info(f"Retrieving chapters for module: {module_id}")
        return self.db.query(Chapter).filter(Chapter.module_id == module_id).order_by(Chapter.order).all()

    def update_chapter(self, chapter_id: str, **kwargs) -> Optional[Chapter]:
        """Update a chapter."""
        content_logger.info(f"Updating chapter: {chapter_id}")
        chapter = self.get_chapter(chapter_id)
        if chapter:
            for key, value in kwargs.items():
                setattr(chapter, key, value)
            self.db.commit()
            self.db.refresh(chapter)
        return chapter

    def delete_chapter(self, chapter_id: str) -> bool:
        """Delete a chapter."""
        content_logger.info(f"Deleting chapter: {chapter_id}")
        chapter = self.get_chapter(chapter_id)
        if chapter:
            self.db.delete(chapter)
            self.db.commit()
            return True
        return False

    def create_content_block(self, chapter_id: str, type: str, content: str,
                             order: int = None, title: str = None, language: str = None,
                             caption: str = None) -> ContentBlock:
        """Create a new content block."""
        content_logger.info(f"Creating content block of type {type} in chapter: {chapter_id}")

        content_block = ContentBlock(
            chapter_id=chapter_id,
            type=type,
            content=content,
            order=order,
            title=title,
            language=language,
            caption=caption
        )

        self.db.add(content_block)
        self.db.commit()
        self.db.refresh(content_block)

        content_logger.info(f"Content block created successfully: {content_block.id}")
        return content_block

    def get_content_block(self, content_block_id: str) -> Optional[ContentBlock]:
        """Get a content block by ID."""
        content_logger.info(f"Retrieving content block: {content_block_id}")
        return self.db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()

    def list_content_blocks_by_chapter(self, chapter_id: str) -> List[ContentBlock]:
        """List all content blocks in a chapter ordered by their sequence."""
        content_logger.info(f"Retrieving content blocks for chapter: {chapter_id}")
        return self.db.query(ContentBlock).filter(ContentBlock.chapter_id == chapter_id).order_by(ContentBlock.order).all()

    def create_citation(self, module_id: str, chapter_id: str, citation_text: str,
                        url: str = None, author: str = None, title: str = None,
                        publication_info: str = None, type: str = None) -> Citation:
        """Create a new citation."""
        content_logger.info(f"Creating citation for chapter: {chapter_id}")

        citation = Citation(
            module_id=module_id,
            chapter_id=chapter_id,
            citation_text=citation_text,
            url=url,
            author=author,
            title=title,
            publication_info=publication_info,
            type=type
        )

        self.db.add(citation)
        self.db.commit()
        self.db.refresh(citation)

        content_logger.info(f"Citation created successfully: {citation.id}")
        return citation

    def get_citation(self, citation_id: str) -> Optional[Citation]:
        """Get a citation by ID."""
        content_logger.info(f"Retrieving citation: {citation_id}")
        return self.db.query(Citation).filter(Citation.id == citation_id).first()

    def list_citations_by_chapter(self, chapter_id: str) -> List[Citation]:
        """List all citations in a chapter."""
        content_logger.info(f"Retrieving citations for chapter: {chapter_id}")
        return self.db.query(Citation).filter(Citation.chapter_id == chapter_id).all()

    def search_content(self, query: str, module_id: str = None) -> List[Dict[str, Any]]:
        """Search across modules, chapters, and content blocks."""
        content_logger.info(f"Searching content for query: {query}")

        # Search in chapters
        chapters_query = self.db.query(Chapter)
        if module_id:
            chapters_query = chapters_query.filter(Chapter.module_id == module_id)

        chapters = chapters_query.filter(
            Chapter.title.contains(query) | Chapter.content.contains(query)
        ).all()

        # Search in content blocks
        content_blocks_query = self.db.query(ContentBlock)
        if module_id:
            content_blocks_query = content_blocks_query.join(Chapter).filter(Chapter.module_id == module_id)

        content_blocks = content_blocks_query.filter(ContentBlock.content.contains(query)).all()

        results = []

        # Add chapters to results
        for chapter in chapters:
            module = self.db.query(Module).filter(Module.id == chapter.module_id).first()
            results.append({
                "id": str(chapter.id),
                "type": "chapter",
                "title": chapter.title,
                "module": module.title if module else "Unknown Module",
                "content_preview": chapter.content[:200] + "..." if len(chapter.content) > 200 else chapter.content,
                "url": f"/{module.slug if module else 'unknown'}/{chapter.slug}"
            })

        # Add content blocks to results
        for block in content_blocks:
            chapter = self.db.query(Chapter).filter(Chapter.id == block.chapter_id).first()
            module = self.db.query(Module).filter(Module.id == chapter.module_id).first() if chapter else None
            results.append({
                "id": str(block.id),
                "type": "content_block",
                "title": block.title or f"{block.type.title()} Block",
                "module": module.title if module else "Unknown Module",
                "chapter": chapter.title if chapter else "Unknown Chapter",
                "content_preview": block.content[:200] + "..." if len(block.content) > 200 else block.content,
                "url": f"/{module.slug if module else 'unknown'}/{chapter.slug}#{block.id}" if module and chapter else "#"
            })

        content_logger.info(f"Search completed with {len(results)} results")
        return results

    def list_content_blocks_by_chapter(self, chapter_id: str) -> List[ContentBlock]:
        """List all content blocks in a chapter ordered by their sequence."""
        content_logger.info(f"Retrieving content blocks for chapter: {chapter_id}")
        return self.db.query(ContentBlock).filter(ContentBlock.chapter_id == chapter_id).order_by(ContentBlock.order).all()