# Phase 0 Research: Vector Store Selection
    2 
    3 ## 1. Research Question
    4 
    5 The feature specification (`spec.md`) names **Qdrant** as the vector database, while multiple code snippets (`create_RAG_corpus`,     
      `VertexAiRagRetrieval`) exclusively use the integrated tooling from the **Google Cloud Vertex AI RAG service**, which includes its own      managed vector store.
    6 
    7 The question is: Which vector store should be the single source of truth for the implementation?
    8 
    9 ## 2. Analysis & Findings
   10 
   11 -   **Existing Code**: The provided Python code (`VertexAiRagRetrieval`, `rag_response`) is already written to work end-to-end with th      Vertex AI RAG service. This includes corpus creation, file ingestion, and querying.
   12 -   **Integration Effort**: Adhering to the spec's mention of Qdrant would require significant deviation from the existing code       
      patterns. It would involve:
   13     1.  Writing new code to manually handle the embedding process.
   14     2.  Integrating the `qdrant-client` library.
   15     3.  Managing a separate Qdrant instance (either self-hosted or cloud).
   16     4.  Replacing the `rag.retrieval_query` calls with manual queries to Qdrant and then passing that context to the LLM.
   17 -   **Managed Service Benefits**: The Vertex AI RAG service is a managed solution that abstracts away much of the complexity of the RA      pipeline. Using its native components, including the internal vector store, simplifies the architecture and reduces maintenance       
      overhead.
   18 -   **Conclusion**: The implementation shown in the code snippets is more aligned with a rapid, managed-service approach. The mention 
      Qdrant in the spec appears to be either a leftover from an earlier design or a misstatement. The path of least resistance and greatest      coherence with the existing codebase is to use the Vertex AI managed store.
   19 
   20 ## 3. Decision
   21 
   22 -   **Decision**: The project will exclusively use the **Vertex AI managed vector store** provided as part of the Vertex AI RAG servic   23 -   **Rationale**: The existing codebase is already built around this managed service. Deviating to use Qdrant would introduce        
      unnecessary complexity, require significant code changes, and contradict the established implementation pattern. The `spec.md` will be      considered out-of-sync on this specific point, and the implementation will follow the code's direction.
   24 -   **Alternatives Considered**:
   25     -   **Use Qdrant**: This was rejected due to the high implementation cost and the fact that a simpler, integrated solution is     
      already in use.
   26     -   **Hybrid Model**: Using both was rejected as it would create a confusing and redundant architecture with no clear benefits. 