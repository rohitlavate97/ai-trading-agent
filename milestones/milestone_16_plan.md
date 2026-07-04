# Milestone 16: Final Integration Tests & Polish

## 1. Business Requirement
Before finalizing the project, we must ensure that the core trading REST APIs function correctly and that the application is fully documented for end-users to run locally.

## 2. Trading/Financial Workflow
Data integrity is critical. We will write automated integration tests to ensure that `GET /api/v1/portfolio` accurately aggregates open positions and cash balances without arithmetic errors.

## 3. Database Design
- We will leverage `pytest-asyncio` and an in-memory SQLite database (or test MySQL DB depending on our config) to run isolated API tests.

## 4. API / Frontend Design
- **Backend Tests**: Create `backend/tests/test_trading_api.py` using `httpx.AsyncClient` to hit the FastAPI app.
- **Frontend Polish**: Make minor CSS tweaks to ensure the responsive grid layout looks perfect on smaller screens and mobile devices.

## 5. Architecture Decisions
- Tests will target the highest value endpoints (`/portfolio`, `/orders`).
- Update the root `README.md` with explicit instructions on how to start the FastAPI backend and Vite frontend concurrently.

## 6. Commit Sequence
1. `chore: add milestone 16 plan`
2. `test(backend): add integration tests for portfolio and orders API`
3. `style(frontend): final CSS polish and responsive tweaks`
4. `docs: update README with run instructions and finish project`
