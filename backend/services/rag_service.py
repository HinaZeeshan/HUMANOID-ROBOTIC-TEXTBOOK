import cohere
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
import logging
from .embedding_service import EmbeddingService
from .database_service import DatabaseService
from ..api.models import SourceCitation
from ..config.settings import settings

class RAGService:
    def __init__(self):
        # Validate Cohere API key before initializing client
        if not settings.COHERE_API_KEY or settings.COHERE_API_KEY.strip() == "" or settings.COHERE_API_KEY == "Jbcuk5UMlPQTL1I4tC45jQwwrdgH2hGc4YsIOFBF":
            logging.warning("Cohere API key is not configured properly. Some features may not work correctly.")
            self.cohere_client = None
        else:
            # Initialize Cohere client for response generation
            self.cohere_client = cohere.Client(settings.COHERE_API_KEY)

        # Initialize other services
        self.embedding_service = EmbeddingService()
        self.database_service = DatabaseService()

    async def query(self, question: str, selected_text: Optional[str] = None,
                   session_id: Optional[str] = None, query_type: str = "full_book"):
        """
        Process a query using RAG (Retrieval Augmented Generation)
        Returns both answer and source citations
        """
        # Create session if not provided
        if not session_id:
            session = self.database_service.create_session()
            session_id = session["id"]
        else:
            session = self.database_service.get_session(session_id)
            if not session:
                session = self.database_service.create_session()
                session_id = session["id"]

        # Search for relevant documents
        relevant_docs = []
        if query_type == "selected_text_only" and selected_text:
            # For selected text only, we'll return the selected text as the context
            relevant_docs = [{
                "text": selected_text,
                "metadata": {"source": "selected_text", "title": "Selected Text", "location": "user_selection", "section_id": "selected"}
            }]
        else:
            # Search in the full book embeddings
            search_results = self.embedding_service.search_similar(question, limit=5)
            relevant_docs = [
                {
                    "text": result["text"],
                    "metadata": result["metadata"]
                }
                for result in search_results
            ]

        # Create context from relevant documents
        context = "\n\n".join([doc["text"] for doc in relevant_docs])

        # Prepare the prompt for Cohere
        prompt = f"""
        Based on the following context, please answer the question.
        If the context doesn't contain enough information to answer the question,
        please say so and provide the best answer you can based on your general knowledge.

        Context:
        {context}

        Question: {question}

        Answer:
        """

        # Generate response using Cohere if client is available
        if self.cohere_client is None:
            answer = "I'm sorry, but I'm currently unable to generate a response. Please make sure your Cohere API key is properly configured in the .env file."
        else:
            try:
                response = self.cohere_client.chat(
                    model="command-r",
                    message=prompt,
                    max_tokens=500,
                    temperature=0.3
                )
                answer = response.text.strip()
            except Exception as e:
                logging.error(f"Error generating response from Cohere: {e}")
                # Fallback response if Cohere API fails
                answer = "I'm sorry, but I'm currently unable to generate a response. Please make sure your Cohere API key is properly configured."

        # Create source citations
        source_citations = []
        for doc in relevant_docs:
            metadata = doc["metadata"]
            source_citations.append(
                SourceCitation(
                    section_id=metadata.get("section_id", "unknown"),
                    title=metadata.get("title", "Unknown"),
                    location=metadata.get("location", "Unknown")
                )
            )

        # Store the query and response in the database
        self.database_service.create_message(
            session_id=session_id,
            role="user",
            content=question
        )

        self.database_service.create_message(
            session_id=session_id,
            role="assistant",
            content=answer,
            source_citations=[cit.model_dump() for cit in source_citations]
        )

        return answer, [cit.model_dump() for cit in source_citations], session_id

    def get_session_history(self, session_id: str):
        """Get the conversation history for a session"""
        messages = self.database_service.get_messages(session_id)
        return messages