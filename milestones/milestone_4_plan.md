# Milestone 4: User Management & Watchlists

## 1. Business Requirement
Users need the ability to construct custom watchlists of financial assets to track performance, news, and agent recommendations. Administrators need an endpoint to view all users registered on the platform.

## 2. Trading/Financial Workflow
A "Watchlist" is the core entry point for most retail and institutional workflows. By saving a list of ticker symbols (e.g., AAPL, NVDA), users can rapidly command the AI agents to analyze a curated subset of the market rather than searching from scratch every time.

## 3. Database Design
- **`watchlists` table**: `id` (UUID, PK), `user_id` (FK -> users.id), `name` (String), `description` (String), `created_at`, `updated_at`.
- **`watchlist_items` table**: `id` (UUID, PK), `watchlist_id` (FK -> watchlists.id), `symbol` (String, e.g. "AAPL", indexed).

## 4. API Design
- `GET /api/v1/users` (Admin only) - List users
- `POST /api/v1/watchlists` - Create a new watchlist
- `GET /api/v1/watchlists` - List my watchlists
- `POST /api/v1/watchlists/{id}/items` - Add a ticker symbol to a watchlist
- `DELETE /api/v1/watchlists/{id}/items/{symbol}` - Remove a ticker symbol

## 5. Architecture Decisions
- SQLAlchemy Relationships will map the one-to-many hierarchy (`User -> Watchlists -> WatchlistItems`).
- Admin capabilities are protected using the `require_role(RoleEnum.ADMIN)` dependency developed in Milestone 2.

## 6. Commit Sequence
1. `feat(watchlists): add Watchlist models and Alembic migration`
2. `feat(watchlists): add Pydantic schemas for watchlists`
3. `feat(watchlists): add watchlist repository/service layer`
4. `feat(watchlists): add user and watchlist routers`
5. `test(watchlists): add tests for watchlist endpoints`
6. `docs(watchlists): update Developer Guide and changelog`
