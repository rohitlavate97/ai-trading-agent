# Changelog

## [Unreleased]
- **Milestone 12: Authentication & state management**: Created frontend `ApiClient`, `AuthContext`, and `ProtectedRoute`. Connected `/login` and `/register` components to backend FastAPI endpoints using JWT.
- **Milestone 11: Frontend layout and routing**: Initialized Vite + React + TS `frontend` app. Set up premium CSS design tokens and layout components (`AuthLayout`, `DashboardLayout`) with `react-router-dom`.
- **Milestone 10: Agentic streaming responses**: Refactored the Supervisor to use `astream_events`, allowing the WebSocket to stream granular JSON chunks for token generation and tool executions (start/end). Moved milestone plans to a root directory folder.
- **Milestone 9: WebSockets base**: Implemented `ConnectionManager` and a real-time `WebSocket /api/v1/ws/chat` endpoint to stream interactions to the Supervisor agent.
- **Milestone 8: Multi-agent routing**: Replaced the basic agent with a LangGraph hierarchical supervisor pattern. Introduced `MarketAgent` and `PortfolioAgent` specialized sub-nodes.
- **Milestone 7: Tools layer implementation**: Added `@tool` decorators for `get_stock_price` and `get_portfolio_summary`, binding them to the LangGraph execution flow using `ToolNode`.
- **Milestone 6: Agentic API base**: Added LangChain/LangGraph dependencies and created a baseline state graph (`AgentState`) connected to a mock LLM node, exposed via `POST /api/v1/agents/chat`.
- **Milestone 5: Portfolio & Order models**: Added Portfolio, Position, and Order models, schemas, and endpoints. Implemented mock order execution logic.
- **Milestone 4: User management & watchlists**: Added Watchlist and WatchlistItem models, schemas, and REST endpoints. Added Admin endpoint for user listing.
- **Milestone 3: Database foundation**: Added Python Qdrant client connection and idempotent script to seed initial admin and test users in MySQL.
- **Milestone 2: Authentication & RBAC**: Added SQLAlchemy models, Alembic migrations, JWT tokens, OAuth2PasswordBearer flows, and RBAC dependencies.
- **Milestone 1: Project setup**: Configured repository structure, `.gitignore`, Docker Compose skeleton, pre-commit hooks, and GitHub Actions for CI.
