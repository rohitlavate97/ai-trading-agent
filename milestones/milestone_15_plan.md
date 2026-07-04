# Milestone 15: Vector Database (RAG) Connection

## 1. Business Requirement
To provide deep insights, the AI agent must analyze unstructured data like company filings, news, or earnings transcripts. We will implement a Retrieval-Augmented Generation (RAG) pipeline using Qdrant.

## 2. Trading/Financial Workflow
When a trader asks, "What did the latest 10-K say about TSLA's supply chain risks?", the agent retrieves relevant semantic chunks from Qdrant, preventing LLM hallucinations and ensuring answers are grounded in facts.

## 3. Database Design
- **Qdrant**: We will configure `QdrantClient` in a local file-based mode (`path="qdrant_data"`) for easy local development without requiring a separate Docker container.

## 4. API / Frontend Design
- N/A

## 5. Architecture Decisions
- Add `qdrant-client` dependency.
- Create `backend/db/vector.py` for database connection logic.
- Create a new tool `search_company_filings` in `backend/agents/tools.py`.
- For this milestone, if the database is empty, the tool will return a seeded dummy response to prove the agent routing works.
- Add the `search_company_filings` tool to the `MarketAgent` node in the Supervisor graph.

## 6. Commit Sequence
1. `chore: add milestone 15 plan`
2. `feat(db): integrate Qdrant vector database client`
3. `feat(agents): implement RAG search tool for company filings`
4. `docs(agents): update Developer Guide and changelog`
