# Phase 0 Research: Vector Store Selection

## 1. Research Question

The feature specification (`spec.md`) names **Qdrant** as the vector database, while multiple code snippets (`create_RAG_corpus`, `VertexAiRagRetrieval`) exclusively use the integrated tooling from the **Google Cloud Vertex AI RAG service**, which includes its own managed vector store.

The question is: Which vector store should be the single source of truth for the implementation?

## 2. Analysis & Findings

-   **Existing Code**: The provided Python code (`VertexAiRagRetrieval`, `rag_response`) is already written to work end-to-end with the Vertex AI RAG service. This includes corpus creation, file ingestion, and querying.
-   **Integration Effort**: Adhering to the spec's mention of Qdrant would require significant deviation from the existing code patterns. It would involve:
    1.  Writing new code to manually handle the embedding process.
    2.  Integrating the `qdrant-client` library.
    3.  Managing a separate Qdrant instance (either self-hosted or cloud).
    4.  Replacing the `rag.retrieval_query` calls with manual queries to Qdrant and then passing that context to the LLM.
-   **Managed Service Benefits**: The Vertex AI RAG service is a managed solution that abstracts away much of the complexity of the RAG pipeline. Using its native components, including the internal vector store, simplifies the architecture and reduces maintenance overhead.
-   **Conclusion**: The implementation shown in the code snippets is more aligned with a rapid, managed-service approach. The mention of Qdrant in the spec appears to be either a leftover from an earlier design or a misstatement. The path of least resistance and greatest coherence with the existing codebase is to use the Vertex AI managed store.

## 3. Decision

-   **Decision**: The project will exclusively use the **Vertex AI managed vector store** provided as part of the Vertex AI RAG service.
-   **Rationale**: The existing codebase is already built around this managed service. Deviating to use Qdrant would introduce unnecessary complexity, require significant code changes, and contradict the established implementation pattern. The `spec.md` will be considered out-of-sync on this specific point, and the implementation will follow the code's direction.
-   **Alternatives Considered**:
    -   **Use Qdrant**: This was rejected due to the high implementation cost and the fact that a simpler, integrated solution is already in use.
    -   **Hybrid Model**: Using both was rejected as it would create a confusing and redundant architecture with no clear benefits.