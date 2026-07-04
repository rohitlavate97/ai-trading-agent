# Milestone 3: Database Foundation & Seed Data

## 1. Business Requirement
Ensure developers have a deterministic, pre-populated database to test the application immediately after spinning up the environment. Establish the Vector DB connection foundation for future RAG and agentic workflows.

## 2. Trading/Financial Workflow
A baseline dataset (such as an Admin user, and standard watchlists or reference data) is required to test financial interactions without having to manually recreate the entire universe of users and static data.

## 3. Database Design
- **Relational (MySQL)**: The `User` table is already created. We will write a seed script to idempotently insert a default admin (`admin@example.com`) and test user (`user@example.com`).
- **Vector (Qdrant)**: Establish the Qdrant connection via the Python client. Document the upcoming collection design (e.g., `company_filings` for RAG).

## 4. API Design
N/A - This is a database initialization milestone.

## 5. Architecture Decisions
- **Seed Script**: A standalone asynchronous Python script (`backend/db/seed.py`) that uses the existing SQLAlchemy async engine and `user_service` to populate data only if it doesn't already exist.
- **Qdrant Client**: Instantiate a global asynchronous Qdrant client in `backend/db/vector.py` based on `.env` configuration.

## 6. Commit Sequence
1. `feat(db): add Qdrant client connection`
2. `feat(db): create idempotent seed data script for initial users`
3. `docs(db): document Vector DB design and update setup guide`
