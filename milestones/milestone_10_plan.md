# Milestone 10: Agentic Streaming Responses

## 1. Business Requirement
Real-time UX requires users to see the agent's thought process (tool execution) and partial text generation immediately, rather than waiting for the entire multi-agent workflow to finish.

## 2. Trading/Financial Workflow
When a user asks to analyze a portfolio and fetch multiple stock prices, the multi-step process can take several seconds. Streaming tool statuses (e.g., "Fetching AAPL...") keeps the user engaged and informed of the progress.

## 3. Database Design
N/A

## 4. API Design
WebSocket `WS /api/v1/ws/chat` payload OUT will change from a single message to a stream of chunks.
- Token Chunk: `{"type": "token", "content": "Hel"}`
- Tool Start: `{"type": "tool_start", "name": "get_stock_price", "input": {"symbol": "AAPL"}}`
- Tool End: `{"type": "tool_end", "name": "get_stock_price", "result": "150.00"}`
- Message End: `{"type": "message_end"}`

## 5. Architecture Decisions
- Update `chat_with_supervisor` in `backend/agents/supervisor.py` to yield a generator of events using LangGraph's `astream_events`.
- Update `websocket_chat` in `backend/api/routers/websockets.py` to iterate over the generator and `websocket.send_text()` the chunked JSON.

## 6. Commit Sequence
1. `chore: move milestone plans to milestones folder`
2. `feat(agents): implement async streaming generator in supervisor`
3. `feat(websockets): stream chunked responses to client`
4. `docs(agents): update Developer Guide and changelog`
