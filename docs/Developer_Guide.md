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

### User Management & Watchlists
- **Architecture**: A RESTful design for managing collections of financial ticker symbols. Uses `selectinload` for efficient eager loading of nested watchlist items in SQLAlchemy.
- **Database**: Relational structure mapping `users` (1) to `watchlists` (N) to `watchlist_items` (N) with `ON DELETE CASCADE`.
- **API**: Endpoints for CRUD operations on watchlists, and an Admin-only `/api/v1/users` list endpoint.

### Portfolio & Order Management
- **Architecture**: Core financial state representing a user's holdings. Mock execution engine handles MARKET orders immediately, affecting cash balances and position averages.
- **Database**: Strict `Numeric(18,4)` field types are used for `cash_balance`, `price`, and `quantity` to avoid floating-point loss. One-to-One mapping for `User` <-> `Portfolio`, One-to-Many for `Portfolio` <-> `Position` and `Order`.
- **API**: `GET /api/v1/portfolio` fetches the account state and positions, `GET /api/v1/orders` fetches trade history, and `POST /api/v1/orders` allows submitting new trades.

### Agentic Subsystem (LangChain/LangGraph)
- **Architecture**: AI agents are orchestrated using `langgraph` state graphs. We implement a **Multi-Agent Supervisor Pattern** where a central routing agent (Supervisor) delegates tasks to specialized sub-agents (`MarketAgent` and `PortfolioAgent`) based on the conversation history.
- **LLM Integration**: Built to wrap `ChatOpenAI` and leverages structured outputs (`with_structured_output`) for deterministic routing. Can be extended to use local models or other providers via LangChain's unified `BaseChatModel`.
- **Tools**: Sub-agents use LangGraph's `create_react_agent` and bind tools like `get_stock_price` (market data mock) and `get_portfolio_summary` (real DB integration). Tool factories dynamically inject the user's `AsyncSession`.
- **API**: The primary interactive channel is the WebSocket endpoint `WS /api/v1/ws/chat?token=<jwt_token>`. It outputs chunked JSON streams (`type: token`, `type: tool_start`, etc.) utilizing LangGraph's `astream_events` to provide real-time visibility into the agent's LLM generation and tool executions. The legacy REST endpoint `POST /api/v1/agents/chat` remains available but is not recommended for interactive chat due to the lack of streaming capabilities. The `ConnectionManager` tracks active WS sessions per user.

### Database Foundation & Vector DB
- **Relational DB (MySQL)**: Handled via SQLAlchemy 2.x and Alembic. A seed script `backend/db/seed.py` is provided to rapidly initialize essential data (admin and default user) during local setups.
- **Vector DB (Qdrant)**: Asynchronous Qdrant client connection is established in `backend/db/vector.py`. Data such as company filings or knowledge base articles will be stored here in separate collections (e.g., `company_filings`), which will be dynamically queried via LangGraph agents for RAG (Retrieval-Augmented Generation) tasks.

## Frontend Architecture
- **Tech Stack**: React + TypeScript built with Vite.
- **Design System**: A vanilla CSS glassmorphic aesthetic defined in `frontend/src/index.css`. Includes CSS variables for themes, typography (`Outfit` font), and standard component utilities.
- **Routing**: `react-router-dom` manages navigation between `AuthLayout` (for public endpoints like `/login` and `/register`) and `DashboardLayout` (for the authenticated `/` app experience).
