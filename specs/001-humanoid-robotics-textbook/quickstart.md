# Quickstart Guide: Humanoid Robotics Book + RAG Chatbot

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Git installed
- Access to Cohere API key
- Access to Qdrant Cloud (free tier)
- Access to Neon Postgres (free tier)

## Development Environment Setup

### Backend Setup (RAG Service)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up backend environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and service URLs
   ```

4. **Install backend dependencies:**
   ```bash
   pip install fastapi uvicorn python-dotenv cohere qdrant-client psycopg2-binary sqlalchemy
   ```

### Frontend Setup (Docusaurus Book)

1. **Set up frontend environment:**
   ```bash
   cd my-textbook
   npm install
   ```

2. **Configure Docusaurus:**
   ```bash
   # Edit docusaurus.config.js with your site configuration
   # Update sidebars.ts with navigation structure
   ```

## Running the Application

### Development Mode

1. **Start the RAG backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn src.api.main:app --reload --port 8000
   ```

2. **Start the Docusaurus frontend:**
   ```bash
   cd my-textbook
   npm start
   ```

3. **Build the RAG index from book content:**
   ```bash
   cd scripts
   python build-rag-index.py
   ```

### Production Mode

1. **Build the frontend:**
   ```bash
   cd my-textbook
   npm run build
   ```

2. **Deploy backend with Docker:**
   ```bash
   cd backend
   docker build -t robotics-book-backend .
   docker run -p 8000:8000 --env-file .env robotics-book-backend
   ```

## Key Components

### Backend API Structure
- `/api/v1/rag` - RAG query endpoints
- `/api/v1/content` - Book content management
- `/api/v1/chat` - Chatbot interaction endpoints

### Frontend Components
- `Chatbot.tsx` - Embedded chatbot component
- `ChatInterface.tsx` - Standalone chat interface
- Docusaurus documentation pages

## Building the RAG Index

1. **Ensure your book content is in `my-textbook/docs/` as Markdown files**
2. **Run the indexing script:**
   ```bash
   python scripts/build-rag-index.py
   ```
3. **The script will:**
   - Parse all Markdown files
   - Chunk content semantically
   - Generate embeddings
   - Store in Qdrant vector database
   - Store metadata in Neon Postgres

## Testing the Integration

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test RAG functionality:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/rag/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is ROS 2?", "context_filter": "module_1"}'
   ```

3. **Check frontend integration:**
   - Visit `http://localhost:3000`
   - Use the embedded chatbot to ask questions about the book content

## Deployment

### GitHub Pages (Frontend)
1. **Push to main branch**
2. **GitHub Actions will automatically build and deploy** (see `.github/workflows/deploy.yml`)

### Backend Deployment
1. **Deploy to a cloud provider supporting Python/containers**
2. **Configure environment variables**
3. **Set up monitoring and logging**

## Common Tasks

### Adding New Content
1. Add new Markdown file to `my-textbook/docs/`
2. Update `sidebars.ts` to include the new content
3. Rebuild RAG index: `python scripts/build-rag-index.py`

### Updating the Chatbot
1. Modify `src/components/Chatbot.tsx` for frontend changes
2. Update backend services in `src/services/` for logic changes
3. Test the integration

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd my-textbook
npm test
```

## Troubleshooting

### Common Issues
- **API rate limits**: Check your Cohere API usage
- **Database connections**: Verify Neon Postgres connection string
- **Vector search**: Ensure Qdrant is properly configured
- **CORS errors**: Check backend CORS settings in `src/api/main.py`

### Environment Variables
Ensure these are properly set in your `.env` file:
- `COHERE_API_KEY` - Cohere API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `NEON_DATABASE_URL` - Neon Postgres connection string
- `BACKEND_CORS_ORIGINS` - Allowed origins for CORS