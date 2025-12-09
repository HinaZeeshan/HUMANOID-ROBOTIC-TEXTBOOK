# API Documentation

This document provides detailed information about the backend API endpoints for the Humanoid Robotics Textbook project.

## Base URL

All API endpoints are prefixed with `/api/v1/` and served from the backend server (typically `http://localhost:8000`).

## Authentication

Currently, the API does not require authentication for basic functionality. All endpoints are publicly accessible during development.

## Endpoints

### RAG Query Endpoint

#### `POST /api/v1/rag/query`

Query the RAG system and get a response based on textbook content.

**Request Body:**
```json
{
  "query": "string",
  "context_filter": "string | null",
  "selected_text_only": "boolean",
  "selected_text": "string | null",
  "max_chunks": "number",
  "cross_module": "boolean"
}
```

**Parameters:**
- `query` (required): The question or query to process
- `context_filter` (optional): Filter results by specific module (e.g., "module-1", "module-2")
- `selected_text_only` (optional): If true, only use the provided selected_text for context
- `selected_text` (optional): Specific text to use as context when selected_text_only is true
- `max_chunks` (optional): Maximum number of content chunks to retrieve (default: 5)
- `cross_module` (optional): If true, perform cross-module search (default: false)

**Response:**
```json
{
  "response": "string",
  "sources": [
    {
      "title": "string",
      "module": "string",
      "chapter": "string",
      "relevance_score": "number"
    }
  ],
  "query_time_ms": "number"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do ROS 2 nodes communicate?",
    "context_filter": "module-1",
    "cross_module": false
  }'
```

**Response:**
```json
{
  "response": "ROS 2 nodes communicate through topics, services, and actions...",
  "sources": [
    {
      "title": "ROS 2 Communication Patterns",
      "module": "Module 1",
      "chapter": "ROS 2 Basics",
      "relevance_score": 0.92
    }
  ],
  "query_time_ms": 150
}
```

### Content Management Endpoints

#### `GET /api/v1/content/modules`

Retrieve a list of all textbook modules.

**Response:**
```json
[
  {
    "id": "string",
    "title": "string",
    "slug": "string",
    "description": "string",
    "order": "number",
    "learning_objectives": ["string"],
    "prerequisites": ["string"]
  }
]
```

#### `GET /api/v1/content/modules/{module_id}/chapters`

Retrieve all chapters for a specific module.

**Path Parameters:**
- `module_id`: The ID of the module

**Response:**
```json
[
  {
    "id": "string",
    "module_id": "string",
    "title": "string",
    "slug": "string",
    "content": "string",
    "order": "number"
  }
]
```

#### `GET /api/v1/content/chapters/{chapter_id}/blocks`

Retrieve all content blocks for a specific chapter.

**Path Parameters:**
- `chapter_id`: The ID of the chapter

**Response:**
```json
[
  {
    "id": "string",
    "chapter_id": "string",
    "type": "string",
    "content": "string",
    "title": "string",
    "order": "number"
  }
]
```

#### `GET /api/v1/content/search`

Search for content across all modules.

**Query Parameters:**
- `q`: Search query string
- `module`: Optional module filter
- `limit`: Maximum number of results (default: 10)

**Response:**
```json
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "module": "string",
      "chapter": "string",
      "content_preview": "string",
      "relevance_score": "number"
    }
  ],
  "total": "number"
}
```

### Health Check Endpoint

#### `GET /api/v1/rag/health`

Check the health status of the RAG service.

**Response:**
```json
{
  "status": "string",
  "timestamp": "string"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request - Invalid input parameters
- `404`: Not Found - Resource does not exist
- `500`: Internal Server Error - Something went wrong on the server

**Error Response Format:**
```json
{
  "detail": "string"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, rate limiting should be configured based on your deployment requirements.

## CORS Policy

The API allows requests from all origins during development. In production, configure CORS to only allow your frontend domain.

## Query Enhancement

The RAG system includes several query enhancement features:

1. **Cross-module Enhancement**: Automatically detects queries that span multiple modules and enhances them for better retrieval
2. **Simulation Enhancement**: Improves queries related to simulation, physics, and sensor data
3. **Context Enhancement**: Adds relevant context based on the current module when applicable

## Search Methods

The system supports different search methods:
- `semantic`: Standard semantic search using vector embeddings
- `hybrid`: Combines semantic search with context filtering
- `cross-module`: Specialized search for multi-module queries