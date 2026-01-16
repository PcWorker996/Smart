
# Flow

This document describes the end-to-end flow for PDF ingestion and question answering.

## 1. Ingestion (PDF Upload)

1. Client uploads a PDF to the API.
2. API stores the file (disk/S3) and creates a document record.
3. API enqueues a background job with the document ID.
4. API returns a `job_id` to the client immediately.

## 2. Background Processing (Worker)

1. Worker pulls the job from the queue.
2. Worker parses the PDF into text.
3. Worker splits text into chunks.
4. Worker generates embeddings for each chunk.
5. Worker stores chunks + embeddings in PostgreSQL (`pgvector`).
6. Worker marks the job as completed (or failed).

## 3. Question Answering (QA)

1. Client sends a question with the document ID.
2. API embeds the question.
3. API retrieves top-k relevant chunks via vector search.
4. API sends the question + retrieved text to Gemini.
5. API returns the answer with citations to the client.

## 4. Status Tracking

- Client can poll a status endpoint using `job_id` until ingestion completes.
- Failed jobs return an error status with a reason for debugging.
