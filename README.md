
# Smart

Enterprise Knowledge Retrieval System for private PDFs. Users upload a document, the system ingests it asynchronously, and questions are answered with citations using retrieval over vector embeddings.

## Architecture (High Level)

- Frontend: React SPA
- API: FastAPI
- Worker: background jobs for PDF parsing and embedding
- Storage: PostgreSQL + `pgvector` for embeddings
- Queue: Redis
- LLM: Google Gemini

See `docs/ARCHITECTURE.md` and `docs/FLOW.md` for details.

## Repository Layout

```
apps/
  backend/    # FastAPI application and worker code
  frontend/   # React application
docs/         # Architecture and decisions
```

## Local Development

1. Start dependencies:
   - `docker compose up` (PostgreSQL + Redis)
2. Configure environment:
   - Create `.env` at repo root with DB credentials (see `.env.example` if present)
3. Run backend:
   - `uvicorn app.main:app --reload` from `apps/backend`

## Testing

- Runtime deps: `apps/backend/requirements.txt`
- Test deps: `apps/backend/requirements-test.txt`

## Notes

- Large PDF ingestion runs in background jobs to keep the API responsive.
- Embeddings are stored once per document; questions retrieve relevant chunks and send them to Gemini.
