# Use pgvector for vector storage

## Status

Accepted

## Context

Vector embeddings need persistent storage with similarity search capabilities. Document chunks are converted to 384-dimensional vectors (via `all-MiniLM-L6-v2`) and must be efficiently queried to find semantically similar content.

Options for vector storage include:
- Dedicated vector databases (Pinecone, Weaviate, Qdrant)
- PostgreSQL with pgvector extension
- In-memory solutions (FAISS, Annoy)

The system already uses PostgreSQL for relational data (documents, metadata, job status). Adding a separate vector database introduces operational complexity, additional infrastructure, and data synchronization challenges.

## Decision

Use **pgvector** extension for PostgreSQL to store and query vector embeddings.

Concretely:
- Store embeddings as `vector(384)` columns in PostgreSQL tables
- Use pgvector's similarity search operators (`<=>` for cosine distance, `<->` for L2 distance)
- Keep document metadata and embeddings in the same database for transactional consistency
- Leverage existing PostgreSQL infrastructure, backups, and monitoring

## Consequences

Positive consequences:
- **Single database**: No need to maintain separate vector database infrastructure or handle cross-system synchronization
- **Transactional consistency**: Document metadata and embeddings are updated atomically
- **Simpler operations**: Existing PostgreSQL backup, monitoring, and deployment workflows apply to vectors
- **Cost-effective**: No additional managed service costs for small-to-medium scale

Negative consequences:
- **Performance ceiling**: pgvector is slower than specialized vector databases at very large scale (millions+ vectors)
- **Limited indexing options**: Fewer index types compared to dedicated vector DBs (only IVFFlat and HNSW available)
- **PostgreSQL dependency**: Requires PostgreSQL 11+ and pgvector extension installation

## Alternatives considered

1. **Use a dedicated vector database (Pinecone, Weaviate)**
   - Better performance at scale and more advanced indexing
   - Adds infrastructure complexity, cost, and data synchronization overhead
   - Overkill for current scale (hundreds to thousands of documents)

2. **Use in-memory vector search (FAISS)**
   - Fastest search performance
   - No persistence, requires rebuilding index on restart
   - Not suitable for production without additional persistence layer

Given the current scale and existing PostgreSQL infrastructure, pgvector provides the best balance of simplicity, cost, and functionality.
