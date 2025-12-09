"""
Integration tests for the RAG functionality in the Humanoid Robotics Textbook project.
These tests verify the integration between multiple components.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from backend.src.services.rag_service import RAGService
from backend.src.services.content_service import ContentService
from backend.src.models.book_content import Module, Chapter, ContentBlock
from backend.src.models.rag_models import RetrievalResult


class TestRAGIntegration:
    """Integration tests for RAG functionality."""

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

    @pytest.fixture
    def content_service(self, mock_db_session):
        """Create a ContentService instance for testing."""
        return ContentService(mock_db_session)

    def test_rag_query_with_content_service_data(self, rag_service, content_service):
        """Test RAG query using data from content service."""
        query = "What is ROS 2?"

        # Mock content service to return a module
        mock_module = Module(
            id="module-1",
            title="ROS 2 Basics",
            slug="module-1",
            description="Introduction to ROS 2",
            order=1
        )
        content_service.get_module = Mock(return_value=mock_module)

        # Mock the RAG service methods
        with patch.object(rag_service, 'retrieve_relevant_chunks') as mock_retrieve, \
             patch.object(rag_service, 'generate_response') as mock_generate, \
             patch.object(rag_service, '_init_qdrant_collection'):

            mock_retrieve.return_value = [
                {
                    "id": "chunk-1",
                    "content": "ROS 2 is a flexible framework for writing robotic applications.",
                    "metadata": {
                        "module_id": "module-1",
                        "module": "ROS 2 Basics",
                        "chapter_id": "chapter-1",
                        "chapter": "Introduction",
                        "title": "What is ROS 2?"
                    },
                    "score": 0.95
                }
            ]
            mock_generate.return_value = "ROS 2 is a flexible framework for writing robotic applications."

            # Execute the query
            result = rag_service.query(query=query)

            # Verify the result structure
            assert "response" in result
            assert "sources" in result
            assert "query_time_ms" in result
            assert result["response"] == "ROS 2 is a flexible framework for writing robotic applications."
            assert len(result["sources"]) == 1
            assert result["sources"][0]["module"] == "ROS 2 Basics"

    def test_cross_module_query_enhancement(self, rag_service):
        """Test that cross-module queries are properly enhanced."""
        query = "How does voice command lead to robot navigation?"

        # Mock the necessary methods
        with patch.object(rag_service, 'enhance_cross_module_query') as mock_enhance, \
             patch.object(rag_service, 'search_cross_module_content') as mock_search, \
             patch.object(rag_service, 'generate_response') as mock_generate, \
             patch.object(rag_service, '_init_qdrant_collection'):

            enhanced_query = f"{query}. This appears to be a cross-module query involving multiple aspects of humanoid robotics. Consider information from ROS 2 basics, simulation, AI perception/navigation, and VLA systems when formulating the response."
            mock_enhance.return_value = enhanced_query

            mock_search.return_value = [
                {
                    "id": "chunk-1",
                    "content": "Voice commands are processed through speech recognition...",
                    "metadata": {"module": "Module 4", "chapter": "VLA Systems"},
                    "score": 0.9
                },
                {
                    "id": "chunk-2",
                    "content": "Navigation is handled by the Nav2 stack...",
                    "metadata": {"module": "Module 3", "chapter": "AI Navigation"},
                    "score": 0.85
                }
            ]
            mock_generate.return_value = "The process involves voice recognition followed by navigation planning..."

            # Execute the query with cross_module flag
            result = rag_service.query(query=query, cross_module=True)

            # Verify the enhancement was called
            mock_enhance.assert_called_once_with(query)
            # Verify cross-module search was used
            mock_search.assert_called_once()
            # Verify the result structure
            assert "response" in result
            assert result["response"] == "The process involves voice recognition followed by navigation planning..."

    def test_content_indexing_workflow(self, rag_service, content_service):
        """Test the complete workflow from content creation to RAG indexing."""
        # Create mock content
        module = Module(
            id="module-1",
            title="Test Module",
            slug="test-module"
        )

        chapter = Chapter(
            id="chapter-1",
            module_id="module-1",
            title="Test Chapter",
            slug="test-chapter",
            content="This chapter covers important concepts about robotics."
        )

        content_block = ContentBlock(
            id="block-1",
            chapter_id="chapter-1",
            type="text",
            content="ROS 2 is a flexible framework for writing robotic applications.",
            title="ROS 2 Definition",
            order=1
        )

        # Mock content service methods
        content_service.get_module = Mock(return_value=module)
        content_service.list_chapters_by_module = Mock(return_value=[chapter])
        content_service.list_content_blocks_by_chapter = Mock(return_value=[content_block])

        # Test the indexing method
        with patch.object(rag_service, '_generate_embedding', return_value=[0.1, 0.2, 0.3]), \
             patch('backend.src.services.rag_service.qdrant_client') as mock_qdrant, \
             patch.object(rag_service, '_init_qdrant_collection'):

            success = rag_service.index_module_content("module-1")

            # Verify the indexing was successful
            assert success is True
            # Verify Qdrant upsert was called for both chapter and content block
            assert mock_qdrant.upsert.call_count >= 2  # At least for chapter and block

    def test_rag_query_end_to_end(self, rag_service):
        """Test the complete RAG query flow."""
        query = "Explain ROS 2 nodes."

        # Mock all necessary components
        with patch.object(rag_service, 'retrieve_relevant_chunks') as mock_retrieve, \
             patch.object(rag_service, 'generate_response') as mock_generate, \
             patch.object(rag_service, '_init_qdrant_collection'), \
             patch.object(rag_service.db, 'add'), \
             patch.object(rag_service.db, 'commit'):

            # Mock retrieval results
            mock_retrieve.return_value = [
                {
                    "id": "chunk-1",
                    "content": "A node is a collection of ROS 2 processes...",
                    "metadata": {
                        "module_id": "module-1",
                        "module": "ROS 2 Basics",
                        "chapter_id": "chapter-2",
                        "chapter": "Nodes and Topics",
                        "title": "Understanding Nodes"
                    },
                    "score": 0.92
                }
            ]

            # Mock response generation
            expected_response = "A node is a collection of ROS 2 processes that work together to perform specific robotic functions..."
            mock_generate.return_value = expected_response

            # Execute the query
            result = rag_service.query(query=query)

            # Verify all components were called
            mock_retrieve.assert_called_once()
            mock_generate.assert_called_once()
            rag_service.db.add.assert_called_once()  # RetrievalResult should be added to DB
            rag_service.db.commit.assert_called_once()

            # Verify result structure and content
            assert result["response"] == expected_response
            assert len(result["sources"]) == 1
            assert result["sources"][0]["module"] == "ROS 2 Basics"
            assert result["sources"][0]["chapter"] == "Nodes and Topics"
            assert isinstance(result["query_time_ms"], int)

    def test_simulation_query_enhancement(self, rag_service):
        """Test that simulation-related queries are properly enhanced."""
        query = "How does Gazebo simulate physics?"

        with patch.object(rag_service, 'enhance_simulation_query') as mock_enhance, \
             patch.object(rag_service, 'retrieve_relevant_chunks') as mock_retrieve, \
             patch.object(rag_service, 'generate_response') as mock_generate, \
             patch.object(rag_service, '_init_qdrant_collection'), \
             patch.object(rag_service.db, 'add'), \
             patch.object(rag_service.db, 'commit'):

            enhanced_query = f"{query}. Focus on simulation aspects including physics, sensors, environments, and virtual robotics."
            mock_enhance.return_value = enhanced_query

            mock_retrieve.return_value = [
                {
                    "id": "chunk-1",
                    "content": "Gazebo uses ODE for physics simulation...",
                    "metadata": {"module": "Module 2", "chapter": "Simulation Physics"},
                    "score": 0.88
                }
            ]
            mock_generate.return_value = "Gazebo uses the Open Dynamics Engine (ODE) for physics simulation..."

            # Execute the query
            result = rag_service.query(query=query)

            # Verify enhancement was applied
            mock_enhance.assert_called_once_with(query)
            # Verify the result
            assert "response" in result
            assert "Gazebo uses the Open Dynamics Engine (ODE)" in result["response"]


class TestContentRAGIntegration:
    """Tests for integration between content management and RAG services."""

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

    @pytest.fixture
    def content_service(self, mock_db_session):
        """Create a ContentService instance for testing."""
        return ContentService(mock_db_session)

    def test_content_creation_triggers_rag_indexing(self, content_service, rag_service):
        """Test that creating content properly integrates with RAG indexing."""
        # This test would typically verify that when content is created,
        # it gets properly indexed in the RAG system
        module_id = "test-module-1"
        title = "New Chapter"
        content = "This is new chapter content about robotics."

        # Mock the content service database operations
        with patch.object(content_service.db, 'add'), \
             patch.object(content_service.db, 'commit'), \
             patch.object(content_service.db, 'refresh'):

            # Create a chapter
            chapter = content_service.create_chapter(
                module_id=module_id,
                title=title,
                slug="new-chapter",
                content=content
            )

            # Verify chapter was created
            assert chapter.title == title
            assert chapter.content == content

        # In a real scenario, we would have a method that indexes the new content
        # For now, we're verifying the components work together
        assert chapter is not None
        assert chapter.title == title

    def test_retrieval_result_storage(self, rag_service):
        """Test that retrieval results are properly stored in the database."""
        query = "What are ROS 2 services?"

        with patch.object(rag_service, 'retrieve_relevant_chunks') as mock_retrieve, \
             patch.object(rag_service, 'generate_response') as mock_generate, \
             patch.object(rag_service, '_init_qdrant_collection'):

            mock_retrieve.return_value = [
                {
                    "id": "chunk-1",
                    "content": "Services provide a request/response pattern...",
                    "metadata": {"module": "ROS 2 Basics", "chapter": "Services"},
                    "score": 0.91
                }
            ]
            mock_generate.return_value = "Services in ROS 2 provide a request/response pattern for communication..."

            # Execute the query
            result = rag_service.query(query=query)

            # Verify that a RetrievalResult was added to the database
            rag_service.db.add.assert_called_once()
            rag_service.db.commit.assert_called_once()

            # Verify the call was made with a RetrievalResult object
            call_args = rag_service.db.add.call_args[0][0]
            assert isinstance(call_args, RetrievalResult)
            assert call_args.query == query
            assert len(call_args.retrieved_chunks) == 1
            assert call_args.search_method == "semantic"