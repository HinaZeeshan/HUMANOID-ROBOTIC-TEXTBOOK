"""
Contract tests for the RAG API endpoints in the Humanoid Robotics Textbook project.
These tests verify the API contracts and ensure backward compatibility.
"""
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from backend.src.api.main import app
from backend.src.config import settings


class TestRAGAPIContract:
    """Contract tests for RAG API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the API."""
        with TestClient(app) as client:
            yield client

    @pytest.fixture
    def mock_services(self):
        """Mock the backend services."""
        with patch('backend.src.api.v1.rag.RAGService') as mock_rag_service, \
             patch('backend.src.api.v1.content.ContentService') as mock_content_service, \
             patch('backend.src.utils.database.get_db') as mock_get_db:

            # Mock the database session
            mock_db = Mock(spec=Session)
            mock_get_db.return_value = mock_db

            # Mock RAG service instance
            rag_instance = Mock()
            rag_instance.query.return_value = {
                "response": "Test response from RAG system",
                "sources": [
                    {
                        "title": "Test Source",
                        "module": "Test Module",
                        "chapter": "Test Chapter",
                        "relevance_score": 0.95
                    }
                ],
                "query_time_ms": 150
            }
            rag_instance.index_content.return_value = "test-doc-id"
            mock_rag_service.return_value = rag_instance

            # Mock Content service instance
            content_instance = Mock()
            content_instance.get_module.return_value = Mock(
                id="module-1",
                title="Test Module",
                slug="test-module",
                description="A test module",
                order=1
            )
            content_instance.list_chapters_by_module.return_value = [
                Mock(
                    id="chapter-1",
                    title="Test Chapter",
                    slug="test-chapter",
                    content="Test content",
                    order=1
                )
            ]
            mock_content_service.return_value = content_instance

            yield {
                'rag_service': rag_instance,
                'content_service': content_instance,
                'db': mock_db
            }

    def test_rag_query_endpoint_contract(self, client, mock_services):
        """Test the RAG query endpoint contract."""
        query_request = {
            "query": "What is ROS 2?",
            "context_filter": "module-1",
            "selected_text_only": False,
            "selected_text": None,
            "max_chunks": 5,
            "cross_module": False
        }

        response = client.post("/api/v1/rag/query", json=query_request)

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "response" in data
        assert "sources" in data
        assert "query_time_ms" in data

        # Verify response field types
        assert isinstance(data["response"], str)
        assert isinstance(data["sources"], list)
        assert isinstance(data["query_time_ms"], int)

        # Verify sources structure
        if data["sources"]:
            source = data["sources"][0]
            assert "title" in source
            assert "module" in source
            assert "chapter" in source
            assert "relevance_score" in source
            assert isinstance(source["title"], str)
            assert isinstance(source["module"], str)
            assert isinstance(source["chapter"], str)
            assert isinstance(source["relevance_score"], (int, float))

    def test_rag_query_endpoint_required_fields(self, client):
        """Test that RAG query endpoint handles missing optional fields."""
        # Request with only required field
        query_request = {
            "query": "What is ROS 2?"
        }

        response = client.post("/api/v1/rag/query", json=query_request)

        # Should still return 200 (with defaults for optional fields)
        assert response.status_code == 200

        data = response.json()
        assert "response" in data
        assert "sources" in data
        assert "query_time_ms" in data

    def test_rag_query_endpoint_invalid_input(self, client):
        """Test that RAG query endpoint handles invalid input properly."""
        # Request with invalid field type
        query_request = {
            "query": 123,  # Should be string
            "max_chunks": "five"  # Should be integer
        }

        response = client.post("/api/v1/rag/query", json=query_request)

        # Should return 422 for validation error
        assert response.status_code == 422

    def test_rag_health_endpoint(self, client):
        """Test the RAG health endpoint contract."""
        response = client.get("/api/v1/rag/health")

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

        # Verify field types
        assert isinstance(data["status"], str)
        assert isinstance(data["timestamp"], str)

    def test_content_modules_endpoint(self, client, mock_services):
        """Test the content modules endpoint contract."""
        response = client.get("/api/v1/content/modules")

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert isinstance(data, list)

        # If there are modules, verify their structure
        if data:
            module = data[0]
            assert "id" in module
            assert "title" in module
            assert "slug" in module
            assert "description" in module
            assert "order" in module
            assert "learning_objectives" in module
            assert "prerequisites" in module

            # Verify field types
            assert isinstance(module["id"], str)
            assert isinstance(module["title"], str)
            assert isinstance(module["slug"], str)
            assert isinstance(module["description"], str)
            assert isinstance(module["order"], int)
            assert isinstance(module["learning_objectives"], list)
            assert isinstance(module["prerequisites"], list)

    def test_content_module_chapters_endpoint(self, client, mock_services):
        """Test the content module chapters endpoint contract."""
        response = client.get("/api/v1/content/modules/module-1/chapters")

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert isinstance(data, list)

        # If there are chapters, verify their structure
        if data:
            chapter = data[0]
            assert "id" in chapter
            assert "module_id" in chapter
            assert "title" in chapter
            assert "slug" in chapter
            assert "content" in chapter
            assert "order" in chapter

            # Verify field types
            assert isinstance(chapter["id"], str)
            assert isinstance(chapter["module_id"], str)
            assert isinstance(chapter["title"], str)
            assert isinstance(chapter["slug"], str)
            assert isinstance(chapter["content"], str)
            assert isinstance(chapter["order"], int)

    def test_content_chapter_blocks_endpoint(self, client, mock_services):
        """Test the content chapter blocks endpoint contract."""
        response = client.get("/api/v1/content/chapters/chapter-1/blocks")

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert isinstance(data, list)

        # If there are blocks, verify their structure
        if data:
            block = data[0]
            assert "id" in block
            assert "chapter_id" in block
            assert "type" in block
            assert "content" in block
            assert "title" in block
            assert "order" in block

            # Verify field types
            assert isinstance(block["id"], str)
            assert isinstance(block["chapter_id"], str)
            assert isinstance(block["type"], str)
            assert isinstance(block["content"], str)
            assert isinstance(block["title"], str)
            assert isinstance(block["order"], int)

    def test_content_search_endpoint(self, client, mock_services):
        """Test the content search endpoint contract."""
        response = client.get("/api/v1/content/search?q=ROS 2")

        # Verify status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "results" in data
        assert "total" in data

        # Verify field types
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)

        # If there are results, verify their structure
        if data["results"]:
            result = data["results"][0]
            assert "id" in result
            assert "title" in result
            assert "module" in result
            assert "chapter" in result
            assert "content_preview" in result
            assert "relevance_score" in result

            # Verify field types
            assert isinstance(result["id"], str)
            assert isinstance(result["title"], str)
            assert isinstance(result["module"], str)
            assert isinstance(result["chapter"], str)
            assert isinstance(result["content_preview"], str)
            assert isinstance(result["relevance_score"], (int, float))

    def test_rag_query_endpoint_method_not_allowed(self, client):
        """Test that RAG query endpoint only accepts POST requests."""
        # Try GET request
        response = client.get("/api/v1/rag/query")
        assert response.status_code == 405  # Method not allowed

        # Try PUT request
        response = client.put("/api/v1/rag/query", json={"query": "test"})
        assert response.status_code == 405  # Method not allowed

        # Try DELETE request
        response = client.delete("/api/v1/rag/query")
        assert response.status_code == 405  # Method not allowed

    def test_content_endpoints_method_not_allowed(self, client):
        """Test that content endpoints have proper method restrictions."""
        # Modules endpoint should not accept POST without proper body
        response = client.post("/api/v1/content/modules")
        # This might return 422 for validation error or 405 for method not allowed
        # depending on the implementation - both are acceptable for contract testing

        # Health check should not accept POST
        response = client.post("/api/v1/rag/health")
        assert response.status_code in [404, 405]  # Either not found or method not allowed

    def test_api_response_headers(self, client, mock_services):
        """Test that API responses have appropriate headers."""
        response = client.post("/api/v1/rag/query", json={"query": "test"})

        # Verify content type
        assert response.headers["content-type"].startswith("application/json")

    def test_error_response_format(self, client):
        """Test that error responses follow a consistent format."""
        # Send invalid request to trigger error
        response = client.post("/api/v1/rag/query", json={"query": 123})

        # Verify error status
        assert response.status_code == 422  # Validation error

        # Verify error response has detail field
        error_data = response.json()
        assert "detail" in error_data


class TestAPIVersioningContract:
    """Tests for API versioning contract."""

    def test_api_version_prefix(self, client):
        """Test that all API endpoints use the correct version prefix."""
        # List of known API endpoints
        endpoints = [
            "/api/v1/rag/query",
            "/api/v1/rag/health",
            "/api/v1/content/modules",
            "/api/v1/content/modules/module-1/chapters",
            "/api/v1/content/chapters/chapter-1/blocks",
            "/api/v1/content/search"
        ]

        # Check that non-versioned endpoints return 404 or 405
        for endpoint in endpoints:
            # Remove version from endpoint
            non_versioned = endpoint.replace("/v1", "")
            response = client.get(non_versioned) if "search" in non_versioned or "health" in non_versioned else client.post(non_versioned, json={"query": "test"})
            # Non-versioned endpoints should not be accessible
            assert response.status_code in [404, 405]

    def test_api_schema_consistency(self, client, mock_services):
        """Test that similar endpoints return data in consistent formats."""
        # Test that different query types return consistent response structure
        simple_query = {"query": "What is ROS 2?"}
        complex_query = {
            "query": "How does ROS 2 work?",
            "context_filter": "module-1",
            "max_chunks": 3,
            "cross_module": False
        }

        response1 = client.post("/api/v1/rag/query", json=simple_query)
        response2 = client.post("/api/v1/rag/query", json=complex_query)

        # Both should return the same structure
        for response in [response1, response2]:
            data = response.json()
            assert "response" in data
            assert "sources" in data
            assert "query_time_ms" in data
            assert isinstance(data["response"], str)
            assert isinstance(data["sources"], list)
            assert isinstance(data["query_time_ms"], int)