# Tasks: RAG Chatbot for Existing Book

**Feature**: RAG Chatbot for Existing Book
**Branch**: 001-rag-chatbot
**Generated**: 2025-12-17
**Input**: User stories from spec.md, architecture from plan.md, API contracts, data models

## Phase 1: Setup Tasks

### Goal
Initialize project structure with all required dependencies and configuration files per the implementation plan.

### Independent Test Criteria
- Project structure matches plan.md specification
- All dependencies can be installed successfully
- Basic server can start without errors
- Basic React app can start without errors

### Implementation Tasks

- [x] T001 Create backend directory structure per plan.md
- [x] T002 Create my-textbook directory structure per plan.md
- [x] T003 [P] Initialize backend/requirements.txt with FastAPI, Cohere SDK, Qdrant, Neon Postgres dependencies
- [x] T004 [P] Initialize my-textbook/package.json with React dependencies
- [x] T005 Create backend/.env.example with required environment variables
- [x] T006 Create backend/main.py with basic FastAPI app structure
- [x] T007 Create my-textbook/src/components/Chatbot directory

## Phase 2: Foundational Tasks

### Goal
Set up core infrastructure: database connections, vector store setup, and basic API framework.

### Independent Test Criteria
- Database connection can be established
- Qdrant connection can be established
- Basic API endpoint responds to requests
- Configuration is properly loaded

### Implementation Tasks

- [x] T008 Setup Neon Postgres database models for ChatSession and ChatMessage
- [x] T009 Create Qdrant collection for book embeddings
- [x] T010 [P] Implement database service in backend/services/database_service.py
- [x] T011 [P] Implement Qdrant service in backend/services/embedding_service.py
- [x] T012 Create API models in backend/api/models.py for requests and responses
- [x] T013 Create settings configuration in backend/config/settings.py
- [x] T014 Test database connection functionality
- [x] T015 Test Qdrant connection functionality

## Phase 3: [US1] Query Book Content via Chat Interface

### Goal
Enable users to ask questions about book content through a chat interface and receive relevant answers based on the book's content with citations.

### Independent Test Criteria
- User can enter a question in the chat interface
- System returns accurate answers based on book content
- Response includes relevant citations to book sections
- System processes queries against vector embeddings

### Implementation Tasks

- [x] T016 [P] [US1] Create MessageBubble component in my-textbook/src/components/Chatbot/MessageBubble.tsx
- [x] T017 [P] [US1] Create MessageInput component in my-textbook/src/components/Chatbot/MessageInput.tsx
- [x] T018 [P] [US1] Create LoadingIndicator component in my-textbook/src/components/Chatbot/LoadingIndicator.tsx
- [x] T019 [US1] Create main Chatbot component in my-textbook/src/components/Chatbot/Chatbot.tsx
- [x] T020 [US1] Implement ingestion pipeline to embed book content into Qdrant
- [x] T021 [P] [US1] Create RAG service in backend/services/rag_service.py
- [x] T022 [US1] Implement /api/query POST endpoint in backend/api/routes.py
- [x] T023 [US1] Connect frontend to call /api/query endpoint
- [ ] T024 [P] [US1] Style Chatbot components with black-gold theme
- [ ] T025 [US1] Make Chatbot responsive for mobile and desktop
- [ ] T026 [US1] Test backend endpoint independently with sample queries
- [ ] T027 [US1] Test full frontend-backend integration for basic queries
- [ ] T028 [US1] Ensure accessibility compliance for chat interface

## Phase 4: [US2] Maintain Conversation Context

### Goal
Preserve and provide access to chat history so users can continue meaningful discussions about complex topics across multiple questions.

### Independent Test Criteria
- Multi-turn conversations maintain context appropriately
- Subsequent questions reference earlier parts of the dialogue
- System understands context and provides relevant responses based on conversation history

### Implementation Tasks

- [x] T029 [US2] Enhance ChatSession model to properly store conversation metadata
- [x] T030 [US2] Update API to maintain session context across requests
- [x] T031 [US2] Implement session creation and retrieval in database service
- [x] T032 [US2] Create GET /api/sessions/{session_id} endpoint
- [ ] T033 [US2] Update Chatbot component to maintain session state
- [ ] T034 [US2] Implement session history display in the chat interface
- [ ] T035 [US2] Test multi-turn conversations with context preservation
- [ ] T036 [US2] Validate conversation context accuracy across multiple exchanges

## Phase 5: [US3] Filter Queries to Specific Book Sections

### Goal
Allow users to limit their queries to particular chapters or sections of the book to get focused answers without irrelevant content.

### Independent Test Criteria
- Users can select specific book sections to query
- Responses only come from selected sections rather than entire book
- System properly filters content based on selected text

### Implementation Tasks

- [x] T037 [US3] Implement selected text capture functionality in Chatbot component
- [x] T038 [US3] Create POST /api/query-selected-text endpoint
- [x] T039 [US3] Update RAG service to support selected-text-only queries
- [x] T040 [US3] Add query type parameter to distinguish between full book and selected text
- [ ] T041 [US3] Implement UI controls for selecting text in MDX content
- [ ] T042 [US3] Test selected text query functionality
- [ ] T043 [US3] Validate that responses only come from selected sections

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper styling, accessibility, and integration with Docusaurus.

### Independent Test Criteria
- All components follow black-gold theme consistently
- All functionality is accessible according to WCAG guidelines
- Chatbot is embedded in relevant MDX pages
- Auto-scroll works when new messages appear

### Implementation Tasks

- [ ] T044 Implement auto-scroll functionality in Chatbot component
- [ ] T045 Embed Chatbot component in relevant MDX pages
- [ ] T046 Add proper error handling for API calls
- [ ] T047 Implement loading states and user feedback
- [ ] T048 Add proper error boundaries and fallback UI
- [ ] T049 Finalize accessibility features (ARIA labels, keyboard navigation)
- [ ] T050 Update docusaurus.config.ts to include Chatbot component
- [ ] T051 Write comprehensive tests for all components and services
- [ ] T052 Perform final integration testing
- [ ] T053 Document the implementation for future maintainers

## Dependencies

User Story 2 (Maintain Conversation Context) depends on foundational setup and basic query functionality from User Story 1.
User Story 3 (Filter Queries to Specific Sections) depends on foundational setup and basic query functionality from User Story 1.

## Parallel Execution Examples

For US1 (P1):
- T016, T017, T018 can run in parallel (different component files)
- T021, T022 can run in parallel (backend service and route)

For US2 (P2):
- T029, T030 can run in parallel (model updates and API updates)

For US3 (P3):
- T037, T038 can run in parallel (frontend capture and backend endpoint)

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1 (Setup), Phase 2 (Foundational), and core tasks in Phase 3 (US1) to achieve the minimum viable product with basic query functionality.

2. **Incremental Delivery**:
   - MVP: Basic chat interface with query functionality (T001-T027)
   - Phase 2: Conversation context (T028-T036)
   - Phase 3: Selected text queries (T037-T043)
   - Phase 4: Polish and accessibility (T044-T053)

3. **Testing Approach**: Each user story is independently testable with clear acceptance criteria as defined in the specification.