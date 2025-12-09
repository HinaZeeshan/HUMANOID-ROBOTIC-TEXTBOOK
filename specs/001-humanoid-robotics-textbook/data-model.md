# Data Model: Humanoid Robotics Book + RAG Chatbot

## Book Content Models

### Module
- **id**: string (UUID) - Unique identifier for the module
- **title**: string - Title of the module (e.g., "ROS 2 Basics")
- **slug**: string - URL-friendly identifier
- **description**: string - Brief description of the module content
- **order**: integer - Sequential order of the module (1-4)
- **word_count**: integer - Estimated word count for the module
- **estimated_time**: integer - Estimated reading time in minutes
- **learning_objectives**: string[] - List of learning objectives
- **prerequisites**: string[] - Prerequisites for this module
- **created_at**: datetime - Creation timestamp
- **updated_at**: datetime - Last updated timestamp

### Chapter
- **id**: string (UUID) - Unique identifier for the chapter
- **module_id**: string (UUID) - Reference to parent module
- **title**: string - Title of the chapter
- **slug**: string - URL-friendly identifier
- **content**: string - Markdown content of the chapter
- **order**: integer - Order within the module
- **word_count**: integer - Word count for the chapter
- **estimated_time**: integer - Estimated reading time in minutes
- **section_headers**: string[] - List of section headers in the chapter
- **diagram_count**: integer - Number of diagrams in the chapter
- **example_count**: integer - Number of code examples in the chapter
- **created_at**: datetime - Creation timestamp
- **updated_at**: datetime - Last updated timestamp

### ContentBlock
- **id**: string (UUID) - Unique identifier for the content block
- **chapter_id**: string (UUID) - Reference to parent chapter
- **type**: enum (text, code, diagram, example, exercise) - Type of content block
- **content**: string - The actual content (markdown or code)
- **order**: integer - Order within the chapter
- **title**: string (optional) - Title for the content block
- **language**: string (optional) - For code blocks (python, cpp, bash, etc.)
- **caption**: string (optional) - Caption for diagrams/examples
- **created_at**: datetime - Creation timestamp
- **updated_at**: datetime - Last updated timestamp

## RAG Models

### DocumentChunk
- **id**: string (UUID) - Unique identifier for the chunk
- **document_id**: string - Reference to the source document (chapter ID)
- **content**: string - The text content of the chunk
- **chunk_index**: integer - Position of this chunk in the document
- **embedding**: float[] - Vector embedding of the content (to be stored in Qdrant)
- **metadata**: object - Additional metadata (source, section, etc.)
  - **source_document**: string - Reference to source document
  - **section_header**: string - Section header this chunk belongs to
  - **module**: string - Module this chunk belongs to
  - **chapter_title**: string - Chapter title
  - **chunk_type**: string - Type of content (text, code, etc.)
- **token_count**: integer - Number of tokens in the chunk
- **created_at**: datetime - Creation timestamp

### ChatSession
- **id**: string (UUID) - Unique identifier for the chat session
- **user_id**: string (optional) - User identifier if authenticated
- **session_token**: string - Anonymous session identifier
- **created_at**: datetime - Session creation timestamp
- **updated_at**: datetime - Last interaction timestamp
- **expires_at**: datetime - Session expiration timestamp
- **title**: string - Auto-generated title based on first query

### ChatMessage
- **id**: string (UUID) - Unique identifier for the message
- **session_id**: string (UUID) - Reference to the chat session
- **role**: enum (user, assistant) - Role of the message sender
- **content**: string - The message content
- **retrieved_context**: string[] - Context chunks retrieved for this message
- **model_used**: string - LLM model used for generation
- **tokens_used**: integer - Number of tokens in the response
- **created_at**: datetime - Message creation timestamp
- **relevance_score**: float - Relevance score of the response (0-1)

### RetrievalResult
- **id**: string (UUID) - Unique identifier for the retrieval result
- **query**: string - Original query
- **retrieved_chunks**: string[] (UUID) - IDs of retrieved document chunks
- **relevance_scores**: float[] - Relevance scores for each chunk
- **search_method**: enum (semantic, keyword, hybrid) - Method used for retrieval
- **latency_ms**: integer - Time taken for retrieval in milliseconds
- **created_at**: datetime - Creation timestamp

## User Models

### User
- **id**: string (UUID) - Unique identifier for the user
- **email**: string (optional) - User's email address
- **name**: string (optional) - User's display name
- **preferences**: object - User preferences
  - **default_model**: string - Preferred LLM model
  - **code_language**: string - Preferred code language examples
  - **difficulty_level**: enum (beginner, intermediate, advanced) - Preferred difficulty
- **created_at**: datetime - Account creation timestamp
- **updated_at**: datetime - Last updated timestamp

## System Models

### Citation
- **id**: string (UUID) - Unique identifier for the citation
- **module_id**: string (UUID) - Reference to the module using this citation
- **chapter_id**: string (UUID) - Reference to the chapter using this citation
- **citation_text**: string - Full APA-formatted citation
- **url**: string (optional) - URL if available
- **accessed_date**: date - Date when the source was accessed
- **type**: enum (book, article, documentation, website) - Type of source
- **author**: string - Author of the source
- **title**: string - Title of the source
- **publication_info**: string - Publication details

## Validation Rules

### Module Validation
- Title must be 5-100 characters
- Order must be between 1-4
- Learning objectives must be 1-5 items
- Estimated time must be > 0 minutes

### Chapter Validation
- Title must be 5-100 characters
- Content must be valid Markdown
- Order must be > 0
- Word count must be > 0

### ContentBlock Validation
- Type must be one of the defined enum values
- Content must not be empty for text/code types
- Language must be specified for code blocks

### DocumentChunk Validation
- Content must be between 100-2000 tokens
- Embedding must be a valid vector array
- Metadata must include required fields

### ChatMessage Validation
- Content must not be empty
- Role must be either 'user' or 'assistant'
- Session ID must reference an existing session

## State Transitions

### Module States
- `draft` → `review` → `published` (content lifecycle)

### ChatSession States
- `active` (created, ongoing conversation)
- `expired` (session timeout reached)
- `archived` (manually archived by user)

## Relationships

### Module → Chapter
- One-to-many relationship (one module has many chapters)

### Chapter → ContentBlock
- One-to-many relationship (one chapter has many content blocks)

### DocumentChunk → RetrievalResult
- Many-to-many relationship through intermediate queries

### ChatSession → ChatMessage
- One-to-many relationship (one session has many messages)

### Module → Citation
- One-to-many relationship (one module has many citations)