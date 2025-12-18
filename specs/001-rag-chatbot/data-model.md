# Data Model: RAG Chatbot for Existing Book

## Entity: ChatSession

**Description**: Represents a single user conversation with the book

**Fields**:
- `id` (string/UUID): Unique identifier for the session
- `created_at` (timestamp): When the session was created
- `updated_at` (timestamp): When the session was last updated
- `user_id` (string, optional): Identifier for the user (if applicable)
- `metadata` (object): Additional session metadata

**Relationships**:
- One-to-many with ChatMessage (one session contains many messages)

**Validation**:
- `id` must be unique
- `created_at` must be in the past
- `updated_at` must be >= `created_at`

## Entity: ChatMessage

**Description**: Individual message within a conversation session

**Fields**:
- `id` (string/UUID): Unique identifier for the message
- `session_id` (string): Foreign key linking to ChatSession
- `role` (string): Either "user" or "assistant"
- `content` (string): The actual message content
- `timestamp` (timestamp): When the message was created
- `source_citations` (array of objects): References to book sections used in response
- `query_context` (object, optional): Context for the query (selected text, etc.)

**Relationships**:
- Many-to-one with ChatSession (many messages belong to one session)

**Validation**:
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `session_id` must reference an existing ChatSession

## Entity: BookSection

**Description**: Identified segments of the book content that can be queried independently

**Fields**:
- `id` (string/UUID): Unique identifier for the book section
- `title` (string): Title of the section
- `content` (string): The actual content of the section
- `location` (string): Path/identifier for where this section exists in the book
- `embedding_id` (string): Reference to the vector embedding in Qdrant
- `metadata` (object): Additional metadata about the section

**Relationships**:
- One-to-many with VectorEmbedding (one section maps to one embedding, but embeddings are stored separately in Qdrant)

**Validation**:
- `id` must be unique
- `content` must not be empty
- `location` must be a valid reference to book content

## Entity: VectorEmbedding

**Description**: Mathematical representation of book content chunks stored in Qdrant for semantic search

**Fields**:
- `id` (string): Unique identifier in Qdrant
- `content_id` (string): Reference to the BookSection
- `embedding` (array of floats): The actual vector embedding
- `metadata` (object): Additional metadata stored with the embedding

**Relationships**:
- Stored separately in Qdrant vector database
- Maps to BookSection via content_id

**Validation**:
- `embedding` must be a valid vector array
- `content_id` must reference an existing BookSection

## Entity: APIRequest

**Description**: Represents an API request to the RAG endpoint

**Fields**:
- `question` (string): The user's question
- `selected_text` (string, optional): Text selected by user for context
- `session_id` (string, optional): Session identifier for context
- `query_type` (string): Either "full_book" or "selected_text_only"

**Validation**:
- `question` must not be empty
- `query_type` must be either "full_book" or "selected_text_only"

## Entity: APIResponse

**Description**: Represents the response from the RAG endpoint

**Fields**:
- `answer` (string): The generated answer to the question
- `source_citations` (array of objects): References to book sections used in response
- `session_id` (string, optional): Session identifier if applicable
- `query_type` (string): Either "full_book" or "selected_text_only"

**Validation**:
- `answer` must not be empty
- `source_citations` must be an array of valid citation objects