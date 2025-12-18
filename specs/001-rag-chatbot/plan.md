# Implementation Plan: RAG Chatbot for Existing Book

**Branch**: `001-rag-chatbot` | **Date**: 2025-12-17 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a RAG chatbot embedded in Docusaurus book with React frontend and FastAPI backend. The system will allow users to ask questions about book content via a chat interface, with responses generated using vector embeddings stored in Qdrant and processed through an OpenAI agent. The solution includes both full-book and selected-text query capabilities with chat session persistence in Neon Postgres.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/JavaScript (frontend React)
**Primary Dependencies**: FastAPI (backend framework), React (frontend), Cohere SDK (RAG), Qdrant (vector store), Neon Postgres (session storage)
**Storage**: Qdrant vector store for embeddings, Neon Postgres for chat sessions
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Docusaurus integration)
**Project Type**: Web (frontend + backend)
**Performance Goals**: <3 second response time for queries, support 100 concurrent users
**Constraints**: REST POST requests only (no WebSocket), responsive design, accessible (WCAG), black-gold theme
**Scale/Scope**: Single book with RAG functionality, multiple concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Technical accuracy: All implementations must be verifiable and backed by official documentation
- Educational clarity: Implementation must be clear for intermediate-to-advanced learners
- Full reproducibility: All code, configurations, and deployment steps must be fully reproducible
- Strict adherence to specified tools: Use only Cohere SDK, FastAPI, Neon Postgres, Qdrant Cloud (free tier) as specified in constitution
- Deployment: GitHub Pages (book) + free-tier hosting (FastAPI backend)

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── api/
│   ├── __init__.py
│   ├── models.py        # Pydantic models for request/response
│   └── routes.py        # API routes for RAG functionality
├── services/
│   ├── __init__.py
│   ├── rag_service.py   # RAG query processing
│   ├── embedding_service.py # Vector embedding operations
│   └── database_service.py # Neon Postgres operations
├── config/
│   ├── __init__.py
│   └── settings.py      # Configuration and settings
└── tests/
    ├── __init__.py
    ├── test_api.py      # API endpoint tests
    └── test_services.py # Service logic tests

my-textbook/
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── Chatbot.tsx
│   │       ├── MessageBubble.tsx
│   │       ├── MessageInput.tsx
│   │       └── LoadingIndicator.tsx
│   └── pages/
├── docusaurus.config.ts # Docusaurus configuration
├── sidebars.ts          # Navigation configuration
├── package.json         # Node.js dependencies
└── tsconfig.json        # TypeScript configuration
```

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
