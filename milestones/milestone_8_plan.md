# Milestone 8: Multi-Agent Routing (Supervisor Agent)

## 1. Business Requirement
As the AI Trading Assistant's capabilities grow, a single agent prompt becomes too complex and brittle. We must implement a multi-agent orchestration layer where a "Supervisor" delegates tasks to specialized sub-agents.

## 2. Trading/Financial Workflow
When a user asks: "How much cash do I have, and what is the price of MSFT?", the Supervisor recognizes two domains. It routes the market query to the Market Agent (which has market tools) and the portfolio query to the Portfolio Agent (which has portfolio tools), then synthesizes the final answer.

## 3. Database Design
N/A - This is purely a LangGraph orchestration update.

## 4. API Design
The existing `POST /api/v1/agents/chat` endpoint remains unchanged in its contract, but its internal implementation will swap out the basic `StateGraph` for the new Supervisor-led graph.

## 5. Architecture Decisions
- **Supervisor Pattern**: We will use LangGraph's hierarchical supervisor pattern.
- **State**: Update `AgentState` to include a `next` field (String) indicating which agent should act next, or `FINISH`.
- **Specialized Agents**:
  - `MarketAgent`: Equipped with `get_stock_price`.
  - `PortfolioAgent`: Equipped with `get_portfolio_summary` (and eventually trading tools).
- **Supervisor**: A specialized LLM node that only decides routing based on the conversation history and available agents.

## 6. Commit Sequence
1. `feat(agents): create specialized market and portfolio agents`
2. `feat(agents): implement Supervisor graph logic`
3. `feat(agents): update api router to use supervisor graph`
4. `docs(agents): update Developer Guide and changelog`
