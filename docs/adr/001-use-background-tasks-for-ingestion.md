# Use background jobs for document ingestion and embedding

## Status

Accepted

## Context

Currently, the document ingestion API keeps the HTTP request open until parsing and embedding complete. This work can take tens of seconds for larger PDFs or complex documents.

This has several downsides:

- The API worker/thread is blocked for the entire duration of parsing and embedding, reducing throughput and limiting the number of concurrent requests it can serve efficiently.
- Many clients, proxies, and load balancers enforce request timeouts in the 30–60 second range; if ingestion exceeds these limits, the request fails even if the server is still working.
- From the user’s perspective, the UI appears stalled because the frontend (e.g., Axios) is waiting on a long‑running response with no visible progress.

The result is a fragile, tightly coupled ingestion flow that does not scale well and is sensitive to timeouts at multiple layers.

## Decision

Long‑running ingestion work (parsing, chunking, and embedding documents, then writing vectors to the store) will be moved off the synchronous request/response path into background jobs executed by dedicated workers.

Concretely:

- The ingestion API endpoint will enqueue a background job that performs parsing, chunking, embedding, and persistence.
- The API will return quickly with an ingestion identifier (or similar token) so the client can track status without holding the HTTP connection open.
- The frontend will treat ingestion as an asynchronous process: it may poll a status endpoint, subscribe to updates, or refresh the document state once processing completes.
- Background workers will run separately from the web API processes, allowing them to scale independently and handle ingestion workloads without blocking request handlers.

This design aligns the ingestion flow with a worker‑queue pattern and enables the use of a task queue library or background‑task mechanism appropriate for the stack (for example, a Python task queue or FastAPI’s background task support).

## Consequences

Positive consequences:

- The API remains responsive because HTTP handlers enqueue work and return quickly instead of blocking on long‑running ingestion.
- Timeouts at clients, proxies, and load balancers are much less likely to be hit, since ingestion is no longer tied to a single long‑lived request.
- Background workers can be scaled horizontally (more workers, separate autoscaling rules) to handle higher ingestion volume without changing the API surface.
- Failures and retries are easier to manage at the job level, improving robustness of the ingestion pipeline.

Negative consequences:

- Additional infrastructure is required: a task queue and broker, plus one or more worker processes that must be deployed, monitored, and maintained.
- The system becomes eventually consistent from the client’s point of view; documents are not immediately available for querying after upload, and the UI must handle “processing” states.
- There is more operational complexity around job visibility (monitoring queues, tracking job status, handling dead letters) compared to a single synchronous request.

## Alternatives considered

1. **Keep ingestion fully synchronous in the API**

   - Simpler to implement, but continues to block API workers, risk timeouts, and degrade user experience for large documents.
   - Does not address scaling concerns as ingestion volume and document size increase.

2. **Split ingestion into multiple smaller synchronous calls**

   - Reduces individual call duration but complicates the client–server contract and increases the number of round trips.
   - Still ties progress to active HTTP requests and does not leverage dedicated workers or a queue.

Given these trade‑offs, using background jobs for document ingestion is preferred to improve scalability, reliability, and user experience.
