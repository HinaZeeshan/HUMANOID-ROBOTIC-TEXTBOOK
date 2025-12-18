# Quickstart Guide: RAG Chatbot for Existing Book

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm/yarn
- Access to Cohere API
- Qdrant Cloud account (or local Qdrant instance)
- Neon Postgres account (or local Postgres instance)

## Setup Backend

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Cohere API key, Qdrant credentials, and Neon Postgres details
   ```

4. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```

## Setup Frontend (Docusaurus)

1. **Navigate to the Docusaurus directory:**
   ```bash
   cd my-textbook
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

## Initialize Vector Store

1. **Run the embedding script to index your book content:**
   ```bash
   cd backend
   python -m scripts.embed_book_content
   ```

## Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
```

## API Endpoints

- `POST /api/query` - Query the book content using RAG
- `POST /api/query-selected-text` - Query specifically selected text
- `GET /api/sessions/{session_id}` - Retrieve a chat session

## Testing the API

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key principles of humanoid locomotion?",
    "query_type": "full_book"
  }'
```

## Integration with Docusaurus

The chatbot component can be embedded in any MDX page using:

```mdx
import Chatbot from '@site/src/components/Chatbot';

<Chatbot />
```

## Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd my-textbook
npm test
```