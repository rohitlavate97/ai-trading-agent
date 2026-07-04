# Milestone 9: WebSockets Base Implementation

## 1. Business Requirement
REST APIs are insufficient for interactive AI chat, where requests can take several seconds to execute (especially multi-agent orchestrations). We must implement bidirectional WebSocket communication to allow for real-time interaction.

## 2. Trading/Financial Workflow
When a user asks the agent to perform complex market analysis, a WebSocket allows the server to instantly acknowledge the request, preventing UI timeouts and providing a smoother user experience.

## 3. Database Design
N/A

## 4. API Design
- `WebSocket /api/v1/ws/chat?token=<jwt>`
- **Authentication**: JWT is passed via the query string because browser WebSocket APIs do not support setting custom `Authorization` headers.
- **Payload IN**: `{"message": "string"}`
- **Payload OUT**: `{"type": "message", "content": "string"}`

## 5. Architecture Decisions
- Create `backend/api/routers/websockets.py`.
- Implement a `ConnectionManager` class to track active connections (foundation for future broadcast capabilities, e.g., price alerts).
- Integrate the existing `chat_with_supervisor` logic to handle the incoming messages. For now, it will return the complete response at once. True token-by-token streaming is deferred to Milestone 10.

## 6. Commit Sequence
1. `feat(websockets): implement ConnectionManager and WS authentication`
2. `feat(websockets): create chat WebSocket endpoint linked to supervisor`
3. `docs(websockets): update Developer Guide and changelog`
