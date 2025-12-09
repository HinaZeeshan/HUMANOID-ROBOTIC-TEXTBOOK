"""
RAG (Retrieval-Augmented Generation) service for the Humanoid Robotics Book + RAG Chatbot project
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import asyncio
from datetime import datetime, timedelta
from uuid import UUID
import hashlib
import json

from backend.src.config import settings
from backend.src.utils.logger import rag_logger
from backend.src.models.rag_models import DocumentChunk, RetrievalResult
from backend.src.utils.database import qdrant_client
from backend.src.services.content_service import ContentService

# Add caching functionality
from functools import wraps
from typing import Callable

# Import Cohere for embeddings and response generation
import cohere


class RAGService:
    """Service for RAG functionality (retrieval and generation)."""

    def __init__(self, db_session: Session):
        self.db = db_session
        self.content_service = ContentService(db_session)
        self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)
        self.collection_name = "book_content_chunks"

        # Add caching for embeddings to improve performance
        self.embedding_cache = {}
        # Add caching for query results to improve performance
        self.query_result_cache = {}
        # Cache TTL in seconds (default 1 hour)
        self.CACHE_TTL = 3600

        # Initialize Qdrant collection if it doesn't exist
        self._init_qdrant_collection()

    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the given text."""
        return hashlib.md5(text.encode()).hexdigest()

    def _get_query_cache_key(self, query: str, context_filter: str = None, cross_module: bool = False, max_chunks: int = 5) -> str:
        """Generate a cache key for the query parameters."""
        cache_params = {
            'query': query,
            'context_filter': context_filter,
            'cross_module': cross_module,
            'max_chunks': max_chunks
        }
        cache_key_str = json.dumps(cache_params, sort_keys=True)
        return hashlib.md5(cache_key_str.encode()).hexdigest()

    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cached item is still valid based on TTL."""
        return (datetime.now() - timestamp).total_seconds() < self.CACHE_TTL

    def _cleanup_cache(self):
        """Remove expired entries from the embedding cache."""
        current_time = datetime.now()
        expired_keys = []

        for key, (_, timestamp) in self.embedding_cache.items():
            if (current_time - timestamp).total_seconds() >= self.CACHE_TTL:
                expired_keys.append(key)

        for key in expired_keys:
            del self.embedding_cache[key]

        if expired_keys:
            rag_logger.info(f"Cleaned up {len(expired_keys)} expired embedding cache entries")

    def _cleanup_query_result_cache(self):
        """Remove expired entries from the query result cache."""
        current_time = datetime.now()
        expired_keys = []

        for key, (_, timestamp) in self.query_result_cache.items():
            if (current_time - timestamp).total_seconds() >= self.CACHE_TTL:
                expired_keys.append(key)

        for key in expired_keys:
            del self.query_result_cache[key]

        if expired_keys:
            rag_logger.info(f"Cleaned up {len(expired_keys)} expired query result cache entries")

    def _init_qdrant_collection(self):
        """Initialize the Qdrant collection for document chunks."""
        try:
            # Check if collection exists
            collections = qdrant_client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with vector configuration
                qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={
                        "content": {
                            "size": 1536,  # Size for text-embedding-ada-002
                            "distance": "Cosine"
                        }
                    }
                )
                rag_logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                rag_logger.info(f"Qdrant collection already exists: {self.collection_name}")
        except Exception as e:
            rag_logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using Cohere with caching."""
        try:
            # Validate input
            if not text or not text.strip():
                raise ValueError("Text cannot be empty or whitespace only")

            if len(text) > 4096:  # Cohere has input limits
                raise ValueError(f"Text is too long: {len(text)} characters. Maximum allowed: 4096")

            # Check if embedding is already cached
            cache_key = self._get_cache_key(text)
            if cache_key in self.embedding_cache:
                cached_result, timestamp = self.embedding_cache[cache_key]
                if self._is_cache_valid(timestamp):
                    rag_logger.debug(f"Embedding cache hit for text: {text[:50]}...")
                    return cached_result

            # Generate new embedding using Cohere
            response = self.cohere_client.embed(
                texts=[text],
                model=settings.embedding_model,
                input_type="search_document"
            )
            embedding = response.embeddings[0]

            # Cache the result
            self.embedding_cache[cache_key] = (embedding, datetime.now())

            rag_logger.debug(f"Generated and cached embedding for text: {text[:50]}...")
            return embedding
        except ValueError as ve:
            rag_logger.error(f"Input validation error generating embedding: {ve}")
            raise
        except Exception as e:
            rag_logger.error(f"Error generating embedding: {e}")
            raise

    def index_content(self, document_id: str, content: str, metadata: Dict[str, Any]) -> str:
        """Index content in Qdrant for retrieval."""
        try:
            # Validate inputs
            if not document_id or not document_id.strip():
                raise ValueError("Document ID cannot be empty or whitespace only")

            if not content or not content.strip():
                raise ValueError("Content cannot be empty or whitespace only")

            if not isinstance(metadata, dict):
                raise ValueError("Metadata must be a dictionary")

            # Generate embedding for the content
            embedding = self._generate_embedding(content)

            # Prepare point for Qdrant
            from qdrant_client.http import models

            point = models.PointStruct(
                id=document_id,
                vector={"content": embedding},
                payload={
                    "content": content,
                    "metadata": metadata
                }
            )

            # Upsert the point to Qdrant
            qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            rag_logger.info(f"Content indexed successfully: {document_id}")
            return document_id
        except ValueError as ve:
            rag_logger.error(f"Input validation error indexing content: {ve}")
            raise
        except Exception as e:
            rag_logger.error(f"Error indexing content: {e}")
            raise

    def retrieve_relevant_chunks(self, query: str, limit: int = 5, context_filter: str = None) -> List[Dict[str, Any]]:
        """Retrieve relevant content chunks based on the query."""
        try:
            # Validate inputs
            if not query or not query.strip():
                raise ValueError("Query cannot be empty or whitespace only")

            if limit <= 0 or limit > 100:  # Set reasonable upper limit
                raise ValueError("Limit must be between 1 and 100")

            # Generate embedding for the query
            query_embedding = self._generate_embedding(query)

            # Prepare search filter if context filter is provided
            search_filter = None
            if context_filter:
                # Validate context filter format
                if not isinstance(context_filter, str) or not context_filter.strip():
                    rag_logger.warning(f"Invalid context filter provided: {context_filter}")
                else:
                    search_filter = models.Filter(
                        must=[
                            models.FieldCondition(
                                key="metadata.module",
                                match=models.MatchValue(value=context_filter)
                            )
                        ]
                    )

            # Search in Qdrant
            search_results = qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=("content", query_embedding),
                query_filter=search_filter,
                limit=limit,
                with_payload=True
            )

            # Format results
            retrieved_chunks = []
            for result in search_results:
                chunk_data = {
                    "id": str(result.id),
                    "content": result.payload.get("content", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                }
                retrieved_chunks.append(chunk_data)

            rag_logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: {query[:50]}...")
            return retrieved_chunks
        except ValueError as ve:
            rag_logger.error(f"Input validation error retrieving chunks: {ve}")
            raise
        except Exception as e:
            rag_logger.error(f"Error retrieving chunks: {e}")
            raise

    def generate_response(self, query: str, context_chunks: List[Dict[str, Any]],
                         selected_text_only: bool = False, selected_text: str = None) -> str:
        """Generate response using Cohere based on the query and context."""
        try:
            # Validate inputs
            if not query or not query.strip():
                raise ValueError("Query cannot be empty or whitespace only")

            if not isinstance(context_chunks, list):
                raise ValueError("Context chunks must be a list")

            if selected_text_only and (not selected_text or not selected_text.strip()):
                raise ValueError("Selected text cannot be empty when selected_text_only is True")

            # Prepare context from retrieved chunks
            if selected_text_only and selected_text:
                # Use only the selected text as context
                context = selected_text
            else:
                # Combine all retrieved chunks as context
                context_parts = []
                for chunk in context_chunks:
                    if not isinstance(chunk, dict):
                        rag_logger.warning("Invalid chunk format in context_chunks, skipping...")
                        continue
                    content = chunk.get("content", "")
                    if content:
                        context_parts.append(content)

                context = "\n\n".join(context_parts)

            # Prepare the prompt for Cohere
            if context:
                # Truncate context if too long (Cohere has token limits)
                max_context_length = 3000  # Adjust based on model's context window
                if len(context) > max_context_length:
                    context = context[:max_context_length]
                    rag_logger.warning(f"Context truncated to {max_context_length} characters to fit model limits")

                prompt = f"""
                You are an expert assistant for the Humanoid Robotics Textbook.
                Answer the user's question based on the provided context from the textbook.
                If the context doesn't contain enough information to answer the question, say so.
                Keep your answers focused on humanoid robotics, ROS 2, simulation, AI perception, and VLA systems.

                Context from textbook:
                {context}

                User question: {query}

                Answer:
                """
            else:
                prompt = f"""
                You are an expert assistant for the Humanoid Robotics Textbook.
                The user asked: {query}

                Unfortunately, I couldn't find relevant information in the textbook to answer this question.
                The Humanoid Robotics Textbook covers ROS 2, Digital Twins, AI-Robot Brain, and Vision-Language-Action systems.

                Answer:
                """

            # Call Cohere API for chat-like response using command-r-plus
            response = self.cohere_client.chat(
                model=settings.default_model,
                message=prompt,
                max_tokens=1000,
                temperature=0.3
            )

            if not response or not response.text:
                raise ValueError("No response generated from Cohere API")

            generated_text = response.text.strip()
            rag_logger.info(f"Generated response for query: {query[:50]}...")

            return generated_text
        except ValueError as ve:
            rag_logger.error(f"Input validation error generating response: {ve}")
            raise
        except Exception as e:
            rag_logger.error(f"Error generating response: {e}")
            raise

    def query(self, query: str, context_filter: str = None, selected_text_only: bool = False,
              selected_text: str = None, max_chunks: int = 5, cross_module: bool = False,
              min_relevance_score: float = 0.3) -> Dict[str, Any]:
        """Main query method that retrieves relevant content and generates a response."""
        start_time = datetime.now()

        try:
            rag_logger.info(f"Processing RAG query: {query[:50]}...")

            # Create cache key for this query
            query_cache_key = self._get_query_cache_key(query, context_filter, cross_module, max_chunks)

            # Check if result is already cached
            if query_cache_key in self.query_result_cache:
                cached_result, timestamp = self.query_result_cache[query_cache_key]
                if self._is_cache_valid(timestamp):
                    rag_logger.debug(f"Query result cache hit for query: {query[:50]}...")
                    return cached_result

            # Clean up caches periodically (every few queries)
            if len(self.embedding_cache) % 10 == 0:  # Clean every 10th query
                self._cleanup_cache()
            if len(self.query_result_cache) % 5 == 0:  # Clean every 5th query
                self._cleanup_query_result_cache()

            # Enhance query if it's a cross-module query
            if cross_module:
                query = self.enhance_cross_module_query(query)
                # Perform cross-module search across all relevant content
                retrieved_chunks = self.search_cross_module_content(
                    query=query,
                    limit=max_chunks,
                    min_relevance_score=min_relevance_score
                )
            else:
                # Retrieve relevant chunks with context filter
                retrieved_chunks = self.retrieve_relevant_chunks(
                    query=query,
                    limit=max_chunks,
                    context_filter=context_filter
                )

            # Filter chunks by minimum relevance score for performance
            if min_relevance_score > 0:
                retrieved_chunks = [chunk for chunk in retrieved_chunks if chunk.get("score", 0) >= min_relevance_score]
                rag_logger.debug(f"Filtered chunks by minimum relevance score ({min_relevance_score}), remaining: {len(retrieved_chunks)}")

            # Generate response using the retrieved context
            response = self.generate_response(
                query=query,
                context_chunks=retrieved_chunks,
                selected_text_only=selected_text_only,
                selected_text=selected_text
            )

            # Calculate query time
            query_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Create retrieval result record
            retrieval_result = RetrievalResult(
                query=query,
                retrieved_chunks=[chunk["id"] for chunk in retrieved_chunks],
                relevance_scores=[chunk["score"] for chunk in retrieved_chunks],
                search_method="cross-module" if cross_module else ("hybrid" if context_filter else "semantic"),
                latency_ms=int(query_time_ms)
            )

            self.db.add(retrieval_result)
            self.db.commit()

            # Prepare sources information
            sources = []
            for chunk in retrieved_chunks:
                metadata = chunk.get("metadata", {})
                sources.append({
                    "title": metadata.get("title", "Untitled"),
                    "module": metadata.get("module", "Unknown Module"),
                    "chapter": metadata.get("chapter", "Unknown Chapter"),
                    "relevance_score": chunk.get("score", 0.0)
                })

            result = {
                "response": response,
                "sources": sources,
                "query_time_ms": int(query_time_ms)
            }

            # Cache the result
            self.query_result_cache[query_cache_key] = (result, datetime.now())
            rag_logger.debug(f"Cached query result for query: {query[:50]}...")

            rag_logger.info(f"RAG query completed successfully in {query_time_ms:.2f}ms")
            return result
        except Exception as e:
            rag_logger.error(f"Error processing RAG query: {e}")
            raise

    def index_module_content(self, module_id: str) -> bool:
        """Index all content of a specific module."""
        try:
            rag_logger.info(f"Indexing content for module: {module_id}")

            # Get the module
            module = self.content_service.get_module(module_id)
            if not module:
                rag_logger.error(f"Module not found: {module_id}")
                return False

            # Get all chapters in the module
            chapters = self.content_service.list_chapters_by_module(module_id)

            indexed_count = 0
            for chapter in chapters:
                # Index the chapter content
                chapter_metadata = {
                    "module_id": str(module.id),
                    "module": module.title,
                    "chapter_id": str(chapter.id),
                    "chapter": chapter.title,
                    "type": "chapter"
                }

                self.index_content(
                    document_id=str(chapter.id),
                    content=chapter.content,
                    metadata=chapter_metadata
                )

                # Get content blocks in the chapter
                content_blocks = self.content_service.list_content_blocks_by_chapter(str(chapter.id))

                for block in content_blocks:
                    block_metadata = {
                        "module_id": str(module.id),
                        "module": module.title,
                        "chapter_id": str(chapter.id),
                        "chapter": chapter.title,
                        "block_id": str(block.id),
                        "block_type": block.type,
                        "type": "content_block"
                    }

                    self.index_content(
                        document_id=str(block.id),
                        content=block.content,
                        metadata=block_metadata
                    )

                indexed_count += 1 + len(content_blocks)  # 1 for chapter + content blocks

            rag_logger.info(f"Indexed {indexed_count} items for module {module.title}")
            return True
        except Exception as e:
            rag_logger.error(f"Error indexing module content: {e}")
            return False

    def enhance_simulation_query(self, query: str) -> str:
        """Enhance queries related to simulation content with domain-specific knowledge."""
        query_lower = query.lower()

        # Check if query is related to simulation
        simulation_keywords = [
            'gazebo', 'unity', 'simulation', 'physics', 'gravity', 'collision',
            'lidar', 'imu', 'depth camera', 'sensor', 'digital twin', 'virtual',
            'render', 'environment', 'world', 'model', 'urdf', 'sdf', 'robotics simulation'
        ]

        if any(keyword in query_lower for keyword in simulation_keywords):
            # Add simulation-specific context to the query
            enhanced_query = f"{query}. Focus on simulation aspects including physics, sensors, environments, and virtual robotics."
            rag_logger.info(f"Enhanced simulation query: {enhanced_query}")
            return enhanced_query

        return query

    def enhance_cross_module_query(self, query: str) -> str:
        """Enhance queries that span multiple modules with integrated context."""
        query_lower = query.lower()

        # Check if query spans multiple modules
        cross_module_indicators = [
            'from.*to', 'then.*to', 'first.*then', 'workflow', 'sequence',
            'integrate', 'combine', 'complete.*task', 'end.*end', 'full.*process',
            'voice.*navigate', 'navigate.*perceive', 'perceive.*manipulate',
            'plan.*execute', 'understand.*act'
        ]

        # Look for cross-module activity patterns
        import re
        for pattern in cross_module_indicators:
            if re.search(pattern, query_lower):
                enhanced_query = f"{query}. This appears to be a cross-module query involving multiple aspects of humanoid robotics. Consider information from ROS 2 basics, simulation, AI perception/navigation, and VLA systems when formulating the response."
                rag_logger.info(f"Enhanced cross-module query: {enhanced_query}")
                return enhanced_query

        return query

    def search_cross_module_content(self, query: str, modules: List[str] = None, limit: int = 10, min_relevance_score: float = 0.3) -> List[Dict[str, Any]]:
        """Search across multiple modules for integrated answers."""
        rag_logger.info(f"Searching across modules for query: {query}")

        # Enhance query for cross-module context
        enhanced_query = self.enhance_cross_module_query(query)

        # Generate embedding for enhanced query
        query_embedding = self._generate_embedding(enhanced_query)

        # Prepare search filter if specific modules are requested
        search_filter = None
        if modules:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.module",
                        match=models.MatchValue(value=mod)
                    ) for mod in modules
                ]
            )

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=("content", query_embedding),
            query_filter=search_filter,
            limit=limit,
            with_payload=True
        )

        # Format results
        retrieved_chunks = []
        for result in search_results:
            chunk_data = {
                "id": str(result.id),
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            }
            retrieved_chunks.append(chunk_data)

        # Filter chunks by minimum relevance score for performance
        if min_relevance_score > 0:
            retrieved_chunks = [chunk for chunk in retrieved_chunks if chunk.get("score", 0) >= min_relevance_score]
            rag_logger.debug(f"Cross-module search filtered by minimum relevance score ({min_relevance_score}), remaining: {len(retrieved_chunks)}")

        rag_logger.info(f"Cross-module search returned {len(retrieved_chunks)} results")
        return retrieved_chunks