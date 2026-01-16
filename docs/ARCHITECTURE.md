# Architecture

## 1. High-Level Overview
This application is a **Enterprise Knowledge Retrieval System** that allows a user to upload a Private PDF and ask questions about it, getting answers based only on that document. It connects to a PostgreSQL database.

The system allows users to:
1.  **Ingest:** Upload PDF documents which are asynchronously chunked, embedded, and indexed.
2.  **Retrieve:** Ask natural language questions and receive accurate answers with source citations.

## 2. System Design (C4 Model)
The system follows a **Modular Monolith** architecture with an **Asynchronous Event-Driven** worker for heavy compute tasks.

* **Frontend**: React (SPA) handling the UI and state management.
* **REST API Layer**: FastAPI acting as the application entry point. It handles Authentication, Validation (Pydantic), and Routing.
* **Worker Layer**: An asynchronous Python worker (Celery/ARQ) that consumes tasks from Redis to handle heavy compute operations (PDF Parsing).
* **Data Layer**: PostgreSQL acting as a hybrid store for both Relational Data (Users) and Vector Embeddings (`pgvector`).

## 3. Code Map
The codebase follows a **Monorepo** structure to centralize full-stack development.

```text
/nexus-rag
├── /apps
│   ├── /backend             # FastAPI Application
│   │   ├── /app             # PRODUCTION SOURCE CODE
│   │   │   ├── /routers     # API Endpoints (Controllers)
│   │   │   ├── /services    # Business Logic (PDF parsing, Vector search)
│   │   │   └── /core        # Config, Database, Logging
│   │   │
│   │   └── /labs            # EXPERIMENTAL CODE (Spikes)
│   │       # Used for testing libraries before integration.
│   │       # Code here is "throwaway" and not production-ready.
│   │
│   └── /frontend            # React Application
│
├── /docs                    # Architecture & Decisions
└── docker-compose.yml       # Infrastructure (DB & Redis only)
```

## 4. Key Design Decisions & Invariants
**A. Modular Monolith over Microservices**
* **Decision:** We run the API and the Worker logic from the same codebase (apps/backend).

* **Reasoning:** Reduces operational complexity (no network latency between services, shared type definitions) while allowing us to scale the Worker independently if needed later.

**B. Async-First Ingestion**
* **Decision:** PDF Uploads do not trigger parsing immediately. They push a "Job Ticket" to Redis.

* **Reasoning:** Parsing a 50MB PDF can take 60+ seconds. Blocking the main HTTP thread would kill server performance. The Redis + Worker pattern ensures the API remains responsive (sub-100ms latency).

**C. Hybrid Database Strategy**
* **Decision:** We use PostgreSQL with pgvector instead of a specialized DB like Pinecone.

* **Reasoning:** Allows "Atomic Transactions." We can delete a User and their Vectors in a single SQL operation, ensuring data consistency without managing two separate databases.

## 5. Tech Stack & Glossary
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL 16
- **Queue**: Redis
- **AI Models**: Gemini
- **DevOps**: Docker Compose