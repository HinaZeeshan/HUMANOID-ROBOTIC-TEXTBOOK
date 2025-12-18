import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import uuid
from ..config.settings import settings
import logging

class EmbeddingService:
    def __init__(self):
        # Initialize Cohere client for embeddings
        self.cohere_client = None
        if settings.COHERE_API_KEY and settings.COHERE_API_KEY.strip() != "" and settings.COHERE_API_KEY != "Jbcuk5UMlPQTL1I4tC45jQwwrdgH2hGc4YsIOFBF":
            try:
                self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
            except Exception as e:
                logging.error(f"Failed to initialize Cohere client: {e}")
        else:
            logging.warning("Cohere API key is not configured properly. Embedding services will use dummy values.")

        # Try to initialize Qdrant client, fallback to in-memory if unavailable
        self.qdrant_client = None
        self.use_qdrant = True
        self._initialize_qdrant()

        # Collection name for book embeddings
        self.collection_name = "book_embeddings"

        # In-memory storage for embeddings when Qdrant is not available
        self._embeddings_store = {}  # {id: {"text": text, "embedding": embedding, "metadata": metadata}}

    def _initialize_qdrant(self):
        """Initialize Qdrant client with error handling"""
        try:
            if settings.QDRANT_URL and settings.QDRANT_API_KEY:
                self.qdrant_client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY
                )
            else:
                self.qdrant_client = QdrantClient(
                    host=settings.QDRANT_HOST,
                    port=settings.QDRANT_PORT
                )
            # Test connection by trying to get collections
            self.qdrant_client.get_collections()
            logging.info("Qdrant connection successful")
        except Exception as e:
            logging.warning(f"Qdrant connection failed: {e}. Using in-memory storage instead.")
            self.use_qdrant = False
            self.qdrant_client = None

    def _create_collection_if_not_exists(self):
        """Create the Qdrant collection if it doesn't already exist"""
        if not self.use_qdrant:
            return  # Skip if using in-memory storage

        try:
            collections = self.qdrant_client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with vector configuration
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
                )
        except Exception as e:
            logging.warning(f"Error checking/creating collection: {e}")
            # Try to create it anyway
            try:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
                )
            except:
                pass  # Collection might already exist

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a text using Cohere"""
        if not self.cohere_client:
             logging.warning("Cohere client not available. returning dummy embedding.")
             return [0.0] * 1024

        try:
            response = self.cohere_client.embed(
                texts=[text],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings[0]
        except Exception as e:
            logging.error(f"Error generating embedding: {e}")
            # Return a dummy embedding if Cohere API fails
            # This allows the system to continue working with a fallback
            return [0.0] * 1024  # Default 1024-dim embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts using Cohere"""
        if not self.cohere_client:
             logging.warning("Cohere client not available. returning dummy embeddings.")
             return [[0.0] * 1024 for _ in texts]

        try:
            response = self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            logging.error(f"Error generating embeddings for multiple texts: {e}")
            # Return dummy embeddings if Cohere API fails
            return [[0.0] * 1024 for _ in texts]  # Default 1024-dim embeddings

    def store_embedding(self, text: str, metadata: Dict, text_id: Optional[str] = None) -> str:
        """Store a text embedding in Qdrant or in-memory storage"""
        if not text_id:
            text_id = str(uuid.uuid4())

        embedding = self.embed_text(text)

        if self.use_qdrant and self.qdrant_client:
            # Store in Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=text_id,
                        vector=embedding,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ]
            )
        else:
            # Store in-memory
            self._embeddings_store[text_id] = {
                "text": text,
                "embedding": embedding,
                "metadata": metadata
            }

        return text_id

    def search_similar(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar texts in Qdrant or in-memory storage"""
        query_embedding = self.embed_text(query)

        if self.use_qdrant and self.qdrant_client:
            # Search in Qdrant
            try:
                results = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=limit
                )

                return [
                    {
                        "id": result.id,
                        "text": result.payload.get("text", ""),
                        "metadata": result.payload.get("metadata", {}),
                        "score": result.score
                    }
                    for result in results
                ]
            except Exception as e:
                logging.warning(f"Qdrant search failed: {e}. Falling back to in-memory search.")
                # Fall back to in-memory search if Qdrant fails
                return self._search_similar_in_memory(query_embedding, limit)
        else:
            # Search in-memory
            return self._search_similar_in_memory(query_embedding, limit)

    def _search_similar_in_memory(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Search for similar texts in in-memory storage using cosine similarity"""
        import math

        def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
            """Calculate cosine similarity between two vectors"""
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(b * b for b in vec2))

            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0

            return dot_product / (magnitude1 * magnitude2)

        # Calculate similarity scores for all stored embeddings
        similarities = []
        for text_id, data in self._embeddings_store.items():
            similarity = cosine_similarity(query_embedding, data["embedding"])
            similarities.append({
                "id": text_id,
                "text": data["text"],
                "metadata": data["metadata"],
                "score": similarity
            })

        # Sort by similarity score in descending order and return top results
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:limit]

    def batch_store_embeddings(self, texts_with_metadata: List[tuple]) -> List[str]:
        """Store multiple text embeddings in Qdrant or in-memory storage"""
        ids = []
        texts = [item[0] for item in texts_with_metadata]
        metadatas = [item[1] for item in texts_with_metadata]

        embeddings = self.embed_texts(texts)

        if self.use_qdrant and self.qdrant_client:
            # Store in Qdrant
            points = []
            for i, (text, metadata, embedding) in enumerate(zip(texts, metadatas, embeddings)):
                text_id = str(uuid.uuid4())
                ids.append(text_id)

                points.append(
                    models.PointStruct(
                        id=text_id,
                        vector=embedding,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                )

            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        else:
            # Store in-memory
            for i, (text, metadata, embedding) in enumerate(zip(texts, metadatas, embeddings)):
                text_id = str(uuid.uuid4())
                ids.append(text_id)

                self._embeddings_store[text_id] = {
                    "text": text,
                    "embedding": embedding,
                    "metadata": metadata
                }

        return ids