#!/usr/bin/env python3
"""
Script to embed book content into Qdrant vector store
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.embedding_service import EmbeddingService
from backend.config.settings import settings
import glob

def read_book_content():
    """
    Read all markdown files from the book documentation
    """
    content_chunks = []

    # Look for documentation in common locations
    doc_paths = [
        "../../my-textbook/docs/**/*.md",
        "../../my-textbook/docs/**/*.mdx",
        "../my-textbook/docs/**/*.md",
        "../my-textbook/docs/**/*.mdx",
        "my-textbook/docs/**/*.md",
        "my-textbook/docs/**/*.mdx"
    ]

    for doc_path in doc_paths:
        md_files = glob.glob(doc_path, recursive=True)
        if md_files:
            for file_path in md_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Split content into chunks (e.g., by sections)
                        chunks = split_content_into_chunks(content, file_path)
                        content_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            break  # Found and processed files, exit the loop

    return content_chunks

def split_content_into_chunks(content, file_path):
    """
    Split content into smaller chunks for embedding
    """
    chunks = []
    chunk_size = 1000  # characters per chunk

    # Split by markdown headers
    parts = content.split('\n## ')

    for i, part in enumerate(parts):
        if len(part.strip()) == 0:
            continue

        # Add header back to each part except the first
        if i > 0:
            part = "## " + part

        # If part is too large, split further
        if len(part) > chunk_size:
            sub_chunks = [part[i:i+chunk_size] for i in range(0, len(part), chunk_size)]
            for j, sub_chunk in enumerate(sub_chunks):
                metadata = {
                    "source_file": file_path,
                    "title": f"Part {i}-{j}",
                    "section_id": f"{Path(file_path).stem}_part_{i}_{j}",
                    "location": f"{file_path}#part-{i}-{j}"
                }
                chunks.append((sub_chunk, metadata))
        else:
            metadata = {
                "source_file": file_path,
                "title": part[:50] + "..." if len(part) > 50 else part[:50],
                "section_id": f"{Path(file_path).stem}_part_{i}",
                "location": f"{file_path}#part-{i}"
            }
            chunks.append((part, metadata))

    return chunks

def main():
    """
    Main function to embed book content
    """
    print("Starting book content embedding process...")

    # Initialize embedding service
    embedding_service = EmbeddingService()

    # Read book content
    print("Reading book content...")
    content_chunks = read_book_content()

    if not content_chunks:
        print("No content found to embed. Please ensure documentation files exist.")
        return

    print(f"Found {len(content_chunks)} content chunks to embed")

    # Store embeddings
    print("Storing embeddings in Qdrant...")
    for i, (chunk, metadata) in enumerate(content_chunks):
        if chunk.strip():  # Only process non-empty chunks
            try:
                embedding_service.store_embedding(chunk, metadata)
                if (i + 1) % 10 == 0:  # Print progress every 10 chunks
                    print(f"Embedded {i + 1}/{len(content_chunks)} chunks")
            except Exception as e:
                print(f"Error embedding chunk {i}: {e}")

    print("Embedding process completed!")

if __name__ == "__main__":
    main()