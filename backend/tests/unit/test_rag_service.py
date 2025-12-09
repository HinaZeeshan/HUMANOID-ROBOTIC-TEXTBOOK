"""
Unit tests for the RAG service in the Humanoid Robotics Textbook project.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from backend.src.services.rag_service import RAGService
from backend.src.models.rag_models import DocumentChunk, RetrievalResult


class TestRAGService:
    """Unit tests for the RAGService class."""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session for testing."""
        return Mock(spec=Session)

    @pytest.fixture
    def rag_service(self, mock_db_session):
        """Create a RAGService instance for testing."""
        with patch('backend.src.services.rag_service.cohere.Client'), \
             patch('backend.src.services.rag_service.qdrant_client'):
            return RAGService(mock_db_session)

    def test_init_rag_service(self, mock_db_session):
        """Test initialization of RAGService."""
        with patch('backend.src.services.rag_service.cohere.Client'), \
             patch('backend.src.services.rag_service.qdrant_client') as mock_qdrant:
            # Mock the get_collections method to return empty collections
            mock_qdrant.get_collections.return_value = Mock()
            mock_qdrant.get_collections.return_value.collections = []

            rag_service = RAGService(mock_db_session)

            assert rag_service.db == mock_db_session
            assert rag_service.collection_name == "book_content_chunks"
            # Verify Qdrant collection initialization was called
            mock_qdrant.get_collections.assert_called()

    def test_generate_embedding(self, rag_service):
        """Test embedding generation."""
        test_text = "This is a test sentence."

        with patch.object(rag_service.cohere_client, 'embed') as mock_embed:
            mock_response = Mock()
            mock_response.embeddings = [[0.1, 0.2, 0.3]]
            mock_embed.return_value = mock_response

            result = rag_service._generate_embedding(test_text)

            assert result == [0.1, 0.2, 0.3]
            mock_embed.assert_called_once()

    def test_index_content(self, rag_service):
        """Test content indexing."""
        document_id = "test_doc_1"
        content = "This is test content."
        metadata = {"module": "test_module", "chapter": "test_chapter"}

        with patch.object(rag_service, '_generate_embedding') as mock_embed, \
             patch.object(rag_service, '_init_qdrant_collection'):
            mock_embed.return_value = [0.1, 0.2, 0.3]

            # Mock Qdrant client
            with patch.object(rag_service, 'cohere_client'), \
                 patch('backend.src.services.rag_service.qdrant_client') as mock_qdrant:
                result = rag_service.index_content(document_id, content, metadata)

                assert result == document_id
                mock_embed.assert_called_once_with(content)
                # Verify upsert was called
                mock_qdrant.upsert.assert_called_once()

    def test_enhance_simulation_query(self, rag_service):
        """Test simulation query enhancement."""
        # Test query that should be enhanced
        simulation_query = "How does Gazebo handle physics simulation?"
        enhanced = rag_service.enhance_simulation_query(simulation_query)
        assert "Focus on simulation aspects" in enhanced

        # Test query that should not be enhanced
        non_simulation_query = "What is ROS 2?"
        not_enhanced = rag_service.enhance_simulation_query(non_simulation_query)
        assert not_enhanced == non_simulation_query

    def test_enhance_cross_module_query(self, rag_service):
        """Test cross-module query enhancement."""
        # Test query that should be enhanced
        cross_module_query = "How does voice command lead to navigation?"
        enhanced = rag_service.enhance_cross_module_query(cross_module_query)
        assert "cross-module query" in enhanced.lower()

        # Test query that should not be enhanced
        single_module_query = "What is a ROS node?"
        not_enhanced = rag_service.enhance_cross_module_query(single_module_query)
        assert not_enhanced == single_module_query


class TestContentService:
    """Unit tests for the ContentService class."""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session for testing."""
        return Mock(spec=Session)

    @pytest.fixture
    def content_service(self, mock_db_session):
        """Create a ContentService instance for testing."""
        from backend.src.services.content_service import ContentService
        return ContentService(mock_db_session)

    def test_create_module(self, content_service):
        """Test module creation."""
        title = "Test Module"
        slug = "test-module"
        description = "A test module"

        # Mock the database operations
        with patch.object(content_service.db, 'add'), \
             patch.object(content_service.db, 'commit'), \
             patch.object(content_service.db, 'refresh'):

            module = content_service.create_module(
                title=title,
                slug=slug,
                description=description,
                order=1
            )

            # Verify the module was created with correct attributes
            assert module.title == title
            assert module.slug == slug
            assert module.description == description
            assert module.order == 1

    def test_get_module(self, content_service):
        """Test module retrieval."""
        module_id = "test-module-id"

        # Mock the query result
        mock_module = Mock()
        mock_module.id = module_id
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_module

        with patch.object(content_service.db, 'query', return_value=mock_query):
            result = content_service.get_module(module_id)
            assert result.id == module_id

    def test_create_chapter(self, content_service):
        """Test chapter creation."""
        module_id = "test-module-id"
        title = "Test Chapter"
        slug = "test-chapter"
        content = "Chapter content"

        # Mock the database operations
        with patch.object(content_service.db, 'add'), \
             patch.object(content_service.db, 'commit'), \
             patch.object(content_service.db, 'refresh'):

            chapter = content_service.create_chapter(
                module_id=module_id,
                title=title,
                slug=slug,
                content=content
            )

            # Verify the chapter was created with correct attributes
            assert chapter.module_id == module_id
            assert chapter.title == title
            assert chapter.slug == slug
            assert chapter.content == content


def test_document_chunk_model():
    """Test DocumentChunk model."""
    from backend.src.models.rag_models import DocumentChunk

    chunk = DocumentChunk(
        id="test-chunk",
        content="Test content",
        embedding=[0.1, 0.2, 0.3],
        metadata={"test": "value"}
    )

    assert chunk.id == "test-chunk"
    assert chunk.content == "Test content"
    assert chunk.embedding == [0.1, 0.2, 0.3]
    assert chunk.metadata == {"test": "value"}


def test_retrieval_result_model():
    """Test RetrievalResult model."""
    from datetime import datetime
    from backend.src.models.rag_models import RetrievalResult

    now = datetime.now()
    result = RetrievalResult(
        query="test query",
        retrieved_chunks=["chunk1", "chunk2"],
        relevance_scores=[0.9, 0.8],
        search_method="semantic",
        latency_ms=100
    )

    assert result.query == "test query"
    assert result.retrieved_chunks == ["chunk1", "chunk2"]
    assert result.relevance_scores == [0.9, 0.8]
    assert result.search_method == "semantic"
    assert result.latency_ms == 100
    assert result.timestamp is not None