# Milestone 7: Tools Layer Implementation

## 1. Business Requirement
The LangGraph agent must transition from a simple conversational bot to a capable assistant that executes actions (reading portfolio states) and fetches live data (stock prices).

## 2. Trading/Financial Workflow
When a user asks about an asset, the agent requires deterministic data (tools) rather than relying on stale LLM training weights. Similarly, giving the agent read-access to the portfolio allows it to give contextual advice ("You have $10,000 cash, enough to buy AAPL").

## 3. Database Design
N/A - the tools will leverage the existing SQLAlchemy `portfolio_service.py`.

## 4. API Design
Internal LangChain `@tool` implementations:
- `get_stock_price(symbol: str) -> dict`: Returns a (mocked for now) real-time stock price and basic metrics.
- `get_portfolio_summary(user_id: str) -> dict`: Returns the total cash and active positions.

## 5. Architecture Decisions
- Tools are declared in `backend/agents/tools.py`.
- We use the `langgraph.prebuilt.ToolNode` to execute tools.
- We bind these tools to the `ChatOpenAI` model using `.bind_tools()`.
- The `AgentState` needs to be updated to track the tool-calling loop (routing back to the LLM after tools execute).

## 6. Commit Sequence
1. `feat(agents): implement market data and portfolio tools`
2. `feat(agents): integrate ToolNode and bind tools to state graph`
3. `docs(agents): update Developer Guide and changelog`
