# Milestone 6: Agentic API Base (LangChain/LangGraph setup)

## 1. Business Requirement
The core functionality of the AI Trading Assistant relies on LLM-powered agents. We must lay the architectural foundation for these agents to process user prompts and orchestrate multi-step workflows.

## 2. Trading/Financial Workflow
Users will chat with the assistant ("What is the current price of AAPL?"). The agent needs a structured environment (LangGraph) to decide whether to search the web, query the database, or return a direct response.

## 3. Database Design
N/A for this foundational milestone. Future milestones will persist conversational state (checkpoints).

## 4. API Design
- `POST /api/v1/agents/chat`: Accepts a JSON body containing `{ "message": "user query" }` and returns the agent's string response.

## 5. Architecture Decisions
- **Framework**: `langgraph` for stateful multi-actor agent workflows, `langchain-core` for standard abstractions.
- **Agent State**: Define a simple `AgentState` `TypedDict` containing a list of messages.
- **Initial Graph**: A very basic `StateGraph` that takes a message, passes it to a placeholder/mock LLM node, and returns a response. The actual LLM integration (OpenAI/Anthropic) will be configurable via `.env` but we will set up the abstractions now.

## 6. Commit Sequence
1. `chore(agents): add LangChain and LangGraph dependencies`
2. `feat(agents): create baseline LangGraph state graph`
3. `feat(agents): add agents API router`
4. `docs(agents): update Developer Guide and changelog`
