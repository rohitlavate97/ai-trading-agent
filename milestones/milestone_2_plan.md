# Milestone 2: Authentication & RBAC

## 1. Business Requirement
Implement secure identity verification to ensure only registered users can access the platform and that administrative routes are protected by Role-Based Access Control (RBAC).

## 2. Trading/Financial Workflow
Financial applications demand rigorous identity checks. A compromised account can lead to unauthorized trades (or in our case, paper trades and leaked strategies). All API calls must verify the user's identity statelessly.

## 3. Database Design
To implement auth without placeholders, we must establish the base SQLAlchemy configuration and the `users` table:
- **`users` table**: `id` (UUID), `email` (string, unique), `hashed_password` (string), `role` (enum: user, admin), `is_active` (boolean), `created_at`, `updated_at`.
*(Note: Alembic will be initialized here, fulfilling the prerequisite for future DB milestones).*

## 4. API Design
- `POST /api/v1/auth/register`: Create a new user account.
- `POST /api/v1/auth/token`: Exchange email/password for JWT access and refresh tokens (OAuth2PasswordBearer flow).
- `GET /api/v1/auth/me`: Retrieve current user profile (protected).

## 5. Architecture Decisions
- **Stateless Auth**: JWT (JSON Web Tokens) will be used to avoid session lookups on every request, reducing latency for high-frequency trading API calls.
- **Security**: Passlib with bcrypt for password hashing.
- **FastAPI Dependencies**: `get_current_user` and `require_role` dependencies to enforce RBAC cleanly across routers.

## 6. Commit Sequence
1. `feat(auth): init database foundation and User model` (Sets up SQLAlchemy async engine & Alembic)
2. `feat(auth): implement JWT and password hashing utilities`
3. `feat(auth): implement Pydantic schemas for auth`
4. `feat(auth): implement auth service and router`
5. `feat(auth-ui): scaffold frontend auth services`
6. `test(auth): add auth unit and API tests`
7. `docs(auth): update developer guide`
