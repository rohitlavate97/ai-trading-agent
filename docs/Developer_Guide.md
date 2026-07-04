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
