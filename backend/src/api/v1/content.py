"""
Content API endpoints for the Humanoid Robotics Book + RAG Chatbot project
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.src.utils.database import get_db
from backend.src.services.content_service import ContentService
from backend.src.models.book_content import Module, Chapter


router = APIRouter()


@router.get("/modules", response_model=List[dict])
async def get_modules(db: Session = Depends(get_db)):
    """Get all book modules."""
    content_service = ContentService(db)
    modules = content_service.list_modules()

    return [
        {
            "id": str(module.id),
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "order": module.order,
            "word_count": module.word_count,
            "estimated_time": module.estimated_time,
            "learning_objectives": module.learning_objectives,
            "prerequisites": module.prerequisites
        }
        for module in modules
    ]


@router.get("/modules/{module_id}", response_model=dict)
async def get_module(module_id: str, db: Session = Depends(get_db)):
    """Get a specific module with its chapters."""
    content_service = ContentService(db)
    module = content_service.get_module(module_id)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    chapters = content_service.list_chapters_by_module(module_id)

    return {
        "id": str(module.id),
        "title": module.title,
        "slug": module.slug,
        "description": module.description,
        "order": module.order,
        "word_count": module.word_count,
        "estimated_time": module.estimated_time,
        "learning_objectives": module.learning_objectives,
        "prerequisites": module.prerequisites,
        "chapters": [
            {
                "id": str(chapter.id),
                "title": chapter.title,
                "slug": chapter.slug,
                "order": chapter.order,
                "word_count": chapter.word_count,
                "estimated_time": chapter.estimated_time,
                "section_headers": chapter.section_headers,
                "diagram_count": chapter.diagram_count,
                "example_count": chapter.example_count
            }
            for chapter in chapters
        ]
    }


@router.get("/chapters/{chapter_id}", response_model=dict)
async def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get a specific chapter with its content and content blocks."""
    content_service = ContentService(db)
    chapter = content_service.get_chapter(chapter_id)

    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    module = content_service.get_module(chapter.module_id)

    content_blocks = content_service.list_content_blocks_by_chapter(chapter_id)
    citations = content_service.list_citations_by_chapter(chapter_id)

    return {
        "id": str(chapter.id),
        "module_id": str(chapter.module_id),
        "module_title": module.title if module else None,
        "title": chapter.title,
        "slug": chapter.slug,
        "content": chapter.content,
        "order": chapter.order,
        "word_count": chapter.word_count,
        "estimated_time": chapter.estimated_time,
        "section_headers": chapter.section_headers,
        "diagram_count": chapter.diagram_count,
        "example_count": chapter.example_count,
        "content_blocks": [
            {
                "id": str(block.id),
                "type": block.type,
                "content": block.content,
                "order": block.order,
                "title": block.title,
                "language": block.language,
                "caption": block.caption
            }
            for block in content_blocks
        ],
        "citations": [
            {
                "id": str(citation.id),
                "citation_text": citation.citation_text,
                "url": citation.url,
                "author": citation.author,
                "title": citation.title,
                "publication_info": citation.publication_info
            }
            for citation in citations
        ]
    }


@router.get("/search", response_model=dict)
async def search_content(
    q: str = Query(..., min_length=1, description="Search query string"),
    module: Optional[str] = Query(None, description="Filter search to specific module"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results to return"),
    db: Session = Depends(get_db)
):
    """Search across all book content."""
    content_service = ContentService(db)
    results = content_service.search_content(query=q, module_id=module)

    # Limit results
    limited_results = results[:limit]

    return {
        "results": limited_results,
        "total_results": len(results),
        "query": q,
        "module_filter": module
    }


@router.post("/search", response_model=dict)
async def search_content_post(
    query: str = Query(..., min_length=1, description="Search query string"),
    module: Optional[str] = Query(None, description="Filter search to specific module"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results to return"),
    db: Session = Depends(get_db)
):
    """Search across all book content (POST endpoint for complex queries)."""
    content_service = ContentService(db)
    results = content_service.search_content(query=query, module_id=module)

    # Limit results
    limited_results = results[:limit]

    return {
        "results": limited_results,
        "total_results": len(results),
        "query": query,
        "module_filter": module
    }


@router.get("/modules/{module_id}/toc", response_model=dict)
async def get_module_toc(module_id: str, db: Session = Depends(get_db)):
    """Get table of contents for a specific module."""
    content_service = ContentService(db)
    module = content_service.get_module(module_id)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    chapters = content_service.list_chapters_by_module(module_id)

    return {
        "module": {
            "id": str(module.id),
            "title": module.title,
            "order": module.order
        },
        "chapters": [
            {
                "id": str(chapter.id),
                "title": chapter.title,
                "order": chapter.order,
                "sections": [
                    {"title": header, "level": 2, "order": idx}
                    for idx, header in enumerate(chapter.section_headers or [])
                ] if chapter.section_headers else []
            }
            for chapter in chapters
        ]
    }