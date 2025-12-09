#!/usr/bin/env python3
"""
Script to build RAG index from book content
This script will parse all Markdown files from the textbook,
chunk the content semantically, generate embeddings,
and store in Qdrant vector database.
"""

import os
import sys
from pathlib import Path
import asyncio
from typing import List, Dict, Any
import logging
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import frontmatter  # For parsing markdown with metadata

# Add the backend src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend/src"))

from backend.src.config import settings
from backend.src.services.rag_service import RAGService
from backend.src.services.content_service import ContentService
from backend.src.utils.database import engine, SessionLocal
from backend.src.models.book_content import Module, Chapter, ContentBlock

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: The text to chunk
        max_chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size

        # If we're not at the end, try to break at a sentence boundary
        if end < len(text):
            # Look for a good break point (sentence or paragraph end)
            snippet = text[start:end]
            last_sentence = max(
                snippet.rfind('. '),
                snippet.rfind('?'),
                snippet.rfind('!'),
                snippet.rfind('\n\n')
            )

            if last_sentence > max_chunk_size // 2:  # Only break if it's not too early
                end = start + last_sentence + 1

        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)

        start = end - overlap if end < len(text) else len(text)

    return chunks


def extract_content_blocks(markdown_content: str) -> List[Dict[str, Any]]:
    """
    Extract different types of content blocks from markdown.

    Args:
        markdown_content: The markdown content to parse

    Returns:
        List of content blocks with type and content
    """
    blocks = []

    # Split content into sections based on headers
    sections = re.split(r'\n##\s+', markdown_content)

    # Process the first section (before any ## headers)
    if sections and sections[0].strip():
        # Extract code blocks
        code_pattern = r'```(\w*)\n(.*?)```'
        code_matches = re.findall(code_pattern, sections[0], re.DOTALL)

        for lang, code in code_matches:
            blocks.append({
                'type': 'code',
                'content': f"```{lang}\n{code}```",
                'title': f'Code Block: {lang}' if lang else 'Code Block'
            })

        # Add the remaining text as content
        clean_text = re.sub(code_pattern, '', sections[0], flags=re.DOTALL).strip()
        if clean_text:
            blocks.append({
                'type': 'text',
                'content': clean_text,
                'title': 'Introduction'
            })

    # Process subsequent sections
    for section in sections[1:]:
        if not section.strip():
            continue

        # Extract the section title
        lines = section.split('\n')
        section_title = lines[0].strip() if lines else "Untitled Section"

        # Extract content from the section
        section_content = '\n'.join(lines[1:]).strip()

        # Extract code blocks
        code_pattern = r'```(\w*)\n(.*?)```'
        code_matches = re.findall(code_pattern, section_content, re.DOTALL)

        for lang, code in code_matches:
            blocks.append({
                'type': 'code',
                'content': f"```{lang}\n{code}```",
                'title': f'{section_title}: {lang} Code'
            })

        # Extract YAML frontmatter blocks if present
        yaml_pattern = r'^---\n(.*?)\n---\n'
        yaml_matches = re.findall(yaml_pattern, section_content, re.DOTALL | re.MULTILINE)

        for yaml_content in yaml_matches:
            blocks.append({
                'type': 'yaml',
                'content': f"---\n{yaml_content}\n---",
                'title': f'{section_title}: YAML Configuration'
            })

        # Remove YAML blocks from content for further processing
        clean_content = re.sub(yaml_pattern, '', section_content, flags=re.DOTALL | re.MULTILINE).strip()

        # Extract any remaining text content
        if clean_content:
            blocks.append({
                'type': 'text',
                'content': clean_content,
                'title': section_title
            })

    return blocks


def process_markdown_file(file_path: Path, rag_service: RAGService, content_service: ContentService):
    """
    Process a single markdown file and index its content.

    Args:
        file_path: Path to the markdown file
        rag_service: RAG service instance
        content_service: Content service instance
    """
    logger.info(f"Processing file: {file_path.name}")

    # Read the markdown file with frontmatter
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        content = post.content
        metadata = post.metadata

    # Create a module if it doesn't exist based on filename
    # Extract module info from filename (e.g., 01-ros2-basics.md)
    filename_parts = file_path.stem.split('-', 2)  # Split into 3 parts: ['01', 'ros2', 'basics']
    if len(filename_parts) >= 2 and filename_parts[0].isdigit():
        module_order = int(filename_parts[0])
        module_slug = f"module-{module_order}"
        module_title = metadata.get('title', f"Module {module_order}")
    else:
        module_order = 1
        module_slug = "module-1"
        module_title = metadata.get('title', "Module 1")

    # Check if module already exists
    db = SessionLocal()
    try:
        existing_module = content_service.get_module_by_slug(module_slug)

        if existing_module:
            module = existing_module
        else:
            module = content_service.create_module(
                title=module_title,
                slug=module_slug,
                description=metadata.get('description', ''),
                order=module_order,
                learning_objectives=metadata.get('learning_objectives', []),
                prerequisites=metadata.get('prerequisites', [])
            )
    finally:
        db.close()

    # Create a chapter for this markdown file
    chapter_slug = file_path.stem
    chapter_title = metadata.get('title', chapter_slug.replace('-', ' ').title())

    db = SessionLocal()
    try:
        # Check if chapter already exists
        existing_chapters = content_service.list_chapters_by_module(str(module.id))
        existing_chapter = next((ch for ch in existing_chapters if ch.slug == chapter_slug), None)

        if existing_chapter:
            chapter = existing_chapter
            # Update content if needed
            content_service.update_chapter(
                chapter.id,
                content=content,
                title=chapter_title
            )
        else:
            chapter = content_service.create_chapter(
                module_id=str(module.id),
                title=chapter_title,
                slug=chapter_slug,
                content=content
            )
    finally:
        db.close()

    # Extract content blocks and index them
    content_blocks = extract_content_blocks(content)

    for i, block in enumerate(content_blocks):
        # Create content block in database
        db = SessionLocal()
        try:
            content_service.create_content_block(
                chapter_id=str(chapter.id),
                type=block['type'],
                content=block['content'],
                order=i,
                title=block['title']
            )
        finally:
            db.close()

        # Index content block in RAG system
        try:
            chunk_metadata = {
                "module_id": str(module.id),
                "module": module.title,
                "chapter_id": str(chapter.id),
                "chapter": chapter.title,
                "block_id": f"{chapter.id}_block_{i}",
                "block_type": block['type'],
                "title": block['title']
            }

            # Chunk the content block
            chunks = chunk_text(block['content'])
            for j, chunk in enumerate(chunks):
                chunk_id = f"{chapter.id}_block_{i}_chunk_{j}"
                rag_service.index_content(
                    document_id=chunk_id,
                    content=chunk,
                    metadata=chunk_metadata
                )
        except Exception as e:
            logger.error(f"Error indexing content block {i} from {file_path.name}: {e}")

    logger.info(f"Successfully processed and indexed: {file_path.name}")


async def build_rag_index():
    """Build the RAG index from book content."""
    logger.info("Starting RAG index build process...")

    # Create database session
    db = SessionLocal()

    try:
        # Initialize services
        rag_service = RAGService(db)
        content_service = ContentService(db)

        source_dir = Path(__file__).parent.parent / "my-textbook" / "docs"
        if not source_dir.exists():
            logger.error(f"Source directory does not exist: {source_dir}")
            return False

        markdown_files = list(source_dir.glob("*.md"))
        logger.info(f"Found {len(markdown_files)} markdown files to process")

        for file_path in markdown_files:
            try:
                process_markdown_file(file_path, rag_service, content_service)
            except Exception as e:
                logger.error(f"Error processing file {file_path.name}: {e}")
                continue

        logger.info("RAG index build completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error during RAG index build: {e}")
        return False
    finally:
        db.close()


def main():
    """Main function to run the RAG index build."""
    # Check if required environment variables are set
    if not settings.cohere_api_key or settings.cohere_api_key == "your-cohere-api-key":
        logger.error("Please set the COHERE_API_KEY environment variable")
        sys.exit(1)

    if not settings.qdrant_url or settings.qdrant_url == "https://your-cluster-url.qdrant.tech":
        logger.error("Please set the QDRANT_URL environment variable")
        sys.exit(1)

    success = asyncio.run(build_rag_index())
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()