# Milestone 12: Authentication & State Management

## 1. Business Requirement
The application must securely authenticate users, manage their sessions via JWT, and restrict access to the dashboard.

## 2. Trading/Financial Workflow
Protecting the user's portfolio and trading history is critical. Users must authenticate before issuing agent commands or viewing sensitive data.

## 3. Database Design
N/A

## 4. API / Frontend Design
- **API Client**: A centralized fetch/axios wrapper that automatically injects the `Authorization: Bearer <token>` header into all outbound requests.
- **Auth Context**: A React Context (`AuthContext`) that manages the global authentication state (`token`, `user`) and exposes methods (`login`, `register`, `logout`).
- **Route Guarding**: A `ProtectedRoute` wrapper component that redirects unauthenticated users to `/login`.

## 5. Architecture Decisions
- Store the JWT securely (for this milestone, `localStorage` is standard; a more secure production app might use HttpOnly cookies, but localStorage + OAuth2PasswordBearer is the FastAPI standard we implemented in Milestone 2).
- Update `Login.tsx` and `Register.tsx` to handle forms state and API calls.
- Define a base API URL in a frontend `.env` or hardcode `http://localhost:8000/api/v1` for dev.

## 6. Commit Sequence
1. `feat(frontend): create API client and AuthContext`
2. `feat(frontend): implement login and register logic`
3. `feat(frontend): add ProtectedRoute and route guards`
4. `docs(frontend): update Developer Guide and changelog`
