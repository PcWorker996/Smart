# Engineering Log

## 2026-01-16
**Focus:** Infrastructure Setup

* **[LEARNING]** Google provide the embedding api,

* **[BLOCKER]** I am working on connecting cursor to the Python interpreter of my virtual environment, and I realize because my monorepo isn't a Python project. I, therefore, need to either use separate window as a single workspace or add the 'backend' as Workspace.

* Note that we enfored this hybrid mode of development that running app on our own laptop and running db service on docker container

* Notice the Kafka and Redis differences: Redis is the to-go choice for this project. Redis provide the physical structure to implement the message queue, while Kafka is much robust and powerful pre-assembled solution

* Understanding the concept of Worker Pattern: workers and brokers

* Celery requires broker like RabbitMQ, Redis, or Amazon SQS



* **[INFRA]** Initialized `docker-compose.yml` for PostgreSQL (pgvector) and Redis.
* **[BLOCKER]** `pgvector` was throwing dimension errors.
    * *Cause:* I initialized the column with 1536 dimensions (OpenAI) but tried to insert 768 (Gemini).
    * *Fix:* Updated the SQL migration to use `vector(768)`.
* **[REFACTOR]** Moved `main.py` inside `apps/backend/app` to fix the "Split Brain" directory structure issue.
* **[SETUP]** Created the Monorepo structure (`apps/backend`, `apps/frontend`).
* **[DOCS]** Drafted `ARCHITECTURE.md` using the C4 Model (Container view).
* **[LEARNING]** Learned that "API Gateway" in a monolith just refers to the FastAPI entry point, not a separate server.