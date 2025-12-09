# Humanoid Robotics Textbook - Documentation

Welcome to the Humanoid Robotics Textbook project! This comprehensive educational platform combines a complete textbook on humanoid robotics with an AI-powered RAG (Retrieval-Augmented Generation) chatbot for interactive learning.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Modules](#modules)
- [API Documentation](#api-documentation)
- [Frontend Components](#frontend-components)
- [RAG System](#rag-system)
- [Development Setup](#development-setup)
- [Deployment](#deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Overview

The Humanoid Robotics Textbook project is designed to provide a comprehensive learning experience covering all aspects of humanoid robotics. The system includes:

- **Complete textbook content**: 5 modules covering ROS 2 basics, Digital Twins, AI perception, Vision-Language-Action systems, and an integrated capstone project
- **Interactive chatbot**: AI-powered assistant that can answer questions based on the textbook content
- **Cross-module querying**: Advanced capability to answer questions that span multiple textbook modules
- **Simulation integration**: Coverage of both Gazebo and Unity simulation environments
- **AI integration**: Implementation of NVIDIA Isaac tools, VSLAM, Nav2, and VLA systems

## Architecture

The system follows a modern microservices architecture with a clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │  External APIs  │
│  (Docusaurus)   │◄──►│   (FastAPI)      │◄──►│  (Cohere, etc)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│   Vector DB     │    │   Content DB     │
│   (Qdrant)      │    │  (PostgreSQL)    │
└─────────────────┘    └──────────────────┘
```

### Key Components:
- **Frontend**: Docusaurus-based documentation site with integrated chatbot
- **Backend**: FastAPI application with RAG services
- **Vector Database**: Qdrant for semantic search and retrieval
- **Content Database**: PostgreSQL for structured content management
- **AI Services**: Cohere for embeddings and content generation

## Modules

The textbook is organized into 5 comprehensive modules:

### Module 1: ROS 2 Basics
- Introduction to Robot Operating System 2
- Nodes, topics, services, and actions
- Python-ROS bridging with rclpy
- URDF and robot modeling

### Module 2: Digital Twin Simulation
- Gazebo and Unity simulation environments
- Physics, gravity, and collision modeling
- Sensor simulation and integration
- Digital twin concepts and implementation

### Module 3: AI-Robot Brain
- NVIDIA Isaac tools and synthetic data generation
- VSLAM (Visual Simultaneous Localization and Mapping)
- Nav2 path planning
- Perception and navigation systems

### Module 4: Vision-Language-Action Systems
- Voice command processing with Whisper
- LLM-to-ROS action planning
- Vision-language integration
- Complete VLA pipeline implementation

### Module 5: Capstone Project
- Integration of all previous modules
- Voice → Plan → Navigate → Perceive → Manipulate workflow
- Complete end-to-end implementation
- Cross-module workflow examples

## API Documentation

### RAG Query API
`POST /api/v1/rag/query`

Query the RAG system and get responses based on textbook content.

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

### Content Management API
`GET /api/v1/content/modules`
`GET /api/v1/content/modules/{module_id}/chapters`
`GET /api/v1/content/chapters/{chapter_id}/blocks`

Manage textbook content with these endpoints.

## Frontend Components

### Chatbot Component
Located at `my-textbook/src/components/Chatbot.tsx`, this component provides:
- Context-aware querying based on current textbook page
- Cross-module query detection
- Real-time conversation interface
- Source attribution for responses

### Advanced Chat Interface
Located at `my-textbook/src/pages/ChatInterface.tsx`, this provides:
- Module filtering options
- Source visibility toggle
- Quick suggestion buttons
- Detailed response attribution
- Cross-module workflow support

## RAG System

The RAG system is the core of the AI-powered learning experience:

### Content Indexing
- Automatic parsing of Markdown files from the textbook
- Content block extraction (text, code, YAML)
- Semantic chunking with overlap for context preservation
- Vector embedding generation using Cohere
- Storage in Qdrant vector database with metadata

### Cross-Module Queries
The system can detect and handle queries that span multiple textbook modules:
- Automatic detection of multi-step workflows
- Enhanced query processing for integrated concepts
- Cross-referenced content retrieval
- Comprehensive response generation

### Query Enhancement
- Simulation-specific query enhancement
- Cross-module query enhancement
- Context-aware response generation
- Source attribution with relevance scoring

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional, for containerization)
- Cohere API key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. Start the backend server:
   ```bash
   python -m src.api.main
   ```

### Frontend Setup
1. Navigate to the textbook directory:
   ```bash
   cd my-textbook
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Content Indexing
After making changes to textbook content, rebuild the RAG index:
```bash
cd scripts
python build-rag-index.py
```

## Deployment

### GitHub Pages
The frontend is configured for GitHub Pages deployment:
```bash
cd my-textbook
npm run deploy
```

### Docker
The project includes Docker configuration:
```bash
cd backend
docker-compose up --build
```

## Testing

Testing infrastructure is configured for:
- Unit tests for backend services
- Integration tests for RAG functionality
- Contract tests for API endpoints
- Frontend component tests

(Testing frameworks will be implemented in future tasks)

## Troubleshooting

### Common Issues

**Chatbot not responding:**
- Verify the backend server is running on port 8000
- Check that your Cohere API key is correctly configured
- Ensure the RAG index has been built with content

**Content not appearing in search:**
- Run the RAG index build script to reindex content
- Verify the content files are in the correct format
- Check that the Qdrant vector database is accessible

**Cross-module queries not working:**
- Verify the backend RAG service is properly configured
- Check that the cross_module parameter is being sent correctly
- Ensure the content has been indexed with proper metadata

## Contributing

The project follows a spec-driven development approach with:
- Comprehensive task tracking in `specs/001-humanoid-robotics-textbook/tasks.md`
- Architecture documentation in `plan.md`
- Feature specifications in `spec.md`
- Prompt History Records in `history/prompts/`
- Architecture Decision Records in `history/adr/`

For more information about contributing, see the project constitution and development guidelines in the `.specify/` directory.