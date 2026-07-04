# Developer Guide

## Architecture Overview
The AI Trading Assistant follows a modular monolith architecture. It is designed around Clean Architecture and SOLID principles.

### Backend (Python/FastAPI)
- Uses asynchronous I/O across the board.
- SQLAlchemy 2.x for ORM, Alembic for migrations.
- Organizes domains into separate modules.
- Agents are orchestrated using LangGraph.

### Frontend (Angular)
- Strict TypeScript.
- RxJS and Signals for reactivity.
- WebSocket integrated for real-time market data updates.

## Testing Strategy
- Pytest and Pytest-asyncio for backend tests.
- Httpx for async FastAPI test client.
- Angular built-in tools for frontend component testing.

## Modules

### Authentication & RBAC
- **Architecture**: Employs stateless JWT tokens utilizing the OAuth2PasswordBearer flow for secure API access.
- **Database**: The `users` table holds basic profile data along with the `hashed_password` (via passlib/bcrypt).
- **Security**: Access roles (`USER` vs `ADMIN`) are enforced natively at the route level via FastAPI dependency injection (`require_role(RoleEnum.ADMIN)`).
- **Testing**: Includes tests for correct JWT validation and password hashing behavior.

### Database Foundation & Vector DB
- **Relational DB (MySQL)**: Handled via SQLAlchemy 2.x and Alembic. A seed script `backend/db/seed.py` is provided to rapidly initialize essential data (admin and default user) during local setups.
- **Vector DB (Qdrant)**: Asynchronous Qdrant client connection is established in `backend/db/vector.py`. Data such as company filings or knowledge base articles will be stored here in separate collections (e.g., `company_filings`), which will be dynamically queried via LangGraph agents for RAG (Retrieval-Augmented Generation) tasks.
