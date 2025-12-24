# Specification: The Vector Brain (Memory)

## Context
The FounderMode agent requires a memory system to store and retrieve research findings. We will implement a vector store using ChromaDB to act as the agent's "Working Memory" (RAG). This allows the agent to ingest facts found during research and semantically query them when writing the investment memo.

## Requirements

### 1. Chroma Manager (`memory/vector_store.py`)
- **Initialization:** Create a persistent ChromaDB client stored locally (`.chroma_db`).
- **Embedding Function:** Use `OpenAIEmbeddings` (via `langchain-openai`) with `text-embedding-3-small`.
- **Collection Management:**
    - Create a collection for each run (or a shared one with metadata filtering).
    - Allow resetting/clearing the collection.

### 2. Fact Ingestion (`add_facts`)
- Input: List of `ResearchFact` objects.
- Logic:
    - Convert facts to documents (content + metadata).
    - Add to ChromaDB collection.
    - Return success status.

### 3. Semantic Retrieval (`query_similar`)
- Input: Query string and `k` (number of results).
- Logic:
    - Perform similarity search.
    - Return list of relevant `ResearchFact` objects with their relevance scores.

### 4. Tool Integration
- Update `TavilySearch` tool to optional auto-save results to memory (or handle this in the graph later). *Decision: Keep tools pure, handle storage in the graph node.*

## Acceptance Criteria
- [ ] `ChromaManager` can initialize and create a collection.
- [ ] `add_facts` successfully stores facts.
- [ ] `query_similar` successfully retrieves the most relevant fact for a query.
- [ ] `OPENAI_API_KEY` is loaded from `.env`.
