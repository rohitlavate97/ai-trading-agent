# Milestone 5: Portfolio & Order Models

## 1. Business Requirement
Users need the ability to view their account balance, currently held asset positions, and a historical ledger of placed orders (trades).

## 2. Trading/Financial Workflow
The `Portfolio` is the financial core for a user, tracking `cash_balance`. When an `Order` (BUY/SELL) is executed, it updates the `cash_balance` and modifies the user's `Position` (holding) in that specific asset (e.g., reducing cash and increasing TSLA shares).

## 3. Database Design
- **`portfolios` table**: `id` (UUID), `user_id` (FK -> users.id, Unique), `cash_balance` (DECIMAL), `created_at`, `updated_at`.
- **`positions` table**: `id` (UUID), `portfolio_id` (FK -> portfolios.id), `symbol` (String), `quantity` (DECIMAL), `average_price` (DECIMAL).
- **`orders` table**: `id` (UUID), `portfolio_id` (FK -> portfolios.id), `symbol` (String), `order_type` (Enum: MARKET, LIMIT), `side` (Enum: BUY, SELL), `quantity` (DECIMAL), `price` (DECIMAL, nullable), `status` (Enum: PENDING, EXECUTED, CANCELLED, REJECTED), `created_at`, `updated_at`.

## 4. API Design
- `GET /api/v1/portfolio` - Fetch the current user's portfolio (with positions).
- `GET /api/v1/orders` - List user's orders.
- `POST /api/v1/orders` - Place a new order (for now, simply records the intent and executes immediately as a mock for development, updating the portfolio).

## 5. Architecture Decisions
- Financial fields (`quantity`, `price`, `cash_balance`) must use SQLAlchemy `Numeric(precision=18, scale=4)` to avoid floating-point inaccuracy.
- Enum classes (`OrderSide`, `OrderType`, `OrderStatus`) will be defined using Python's `enum` module and mapped to SQLAlchemy.

## 6. Commit Sequence
1. `feat(portfolio): add Portfolio, Position, Order models and migration`
2. `feat(portfolio): add Pydantic schemas`
3. `feat(portfolio): add portfolio service layer`
4. `feat(portfolio): add portfolio and order routers`
5. `test(portfolio): add tests for portfolio endpoints`
6. `docs(portfolio): update Developer Guide and changelog`
