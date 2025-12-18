import json
from fastapi import APIRouter
from .models import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Endpoint to query the book content using RAG (Retrieval Augmented Generation)
    """
    from ..services.rag_service import RAGService
    rag_service = RAGService()
    answer, source_citations, session_id = await rag_service.query(request.question, request.selected_text, request.session_id, request.query_type)
    return QueryResponse(
        answer=answer,
        source_citations=source_citations,
        session_id=session_id
    )

@router.post("/query-selected-text", response_model=QueryResponse)
async def query_selected_text_endpoint(request: QueryRequest):
    """
    Endpoint to query specifically selected text in the book
    """
    from ..services.rag_service import RAGService
    rag_service = RAGService()
    # Force query type to selected_text_only for this endpoint
    answer, source_citations, session_id = await rag_service.query(request.question, request.selected_text, request.session_id, "selected_text_only")
    return QueryResponse(
        answer=answer,
        source_citations=source_citations,
        session_id=session_id
    )

@router.get("/sessions/{session_id}", response_model=dict)
async def get_session(session_id: str):
    """
    Retrieve a specific chat session with its messages
    """
    from ..services.rag_service import RAGService
    rag_service = RAGService()
    messages = rag_service.get_session_history(session_id)

    # Convert SQLAlchemy objects to dictionaries
    message_list = []
    for msg in messages:
        # Check if msg is a dict or object (handle both for safety)
        if isinstance(msg, dict):
            # Parse source_citations if it's a JSON string
            citations = []
            citations_json = msg.get("source_citations_json") 
            if citations_json:
                 try:
                     citations = json.loads(citations_json) if isinstance(citations_json, str) else citations_json
                 except:
                     pass
            # If source_citations is already a list (from our in-memory DB)
            if "source_citations" in msg and isinstance(msg["source_citations"], list):
                 citations = msg["source_citations"]

            message_list.append({
                "id": msg.get("id"),
                "role": msg.get("role"),
                "content": msg.get("content"),
                "timestamp": msg.get("timestamp"), # In-memory DB stores ISO string
                "source_citations": citations,
            })
        else:
            # Assume SQLAlchemy object
            message_list.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                "source_citations": json.loads(msg.source_citations_json) if msg.source_citations_json and msg.source_citations_json.startswith('[') else [],
            })

    return {
        "session_id": session_id,
        "messages": message_list
    }