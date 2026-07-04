# Milestone 13: AI Chat Widget

## 1. Business Requirement
The core feature of the application is interacting with the AI agent. We must build a robust, real-time chat interface that connects to our backend WebSocket endpoint and processes streaming chunks.

## 2. Trading/Financial Workflow
When analyzing a portfolio or fetching stock prices, the AI takes time. The UI must render `tool_start` events (e.g., "Analyzing TSLA...") to provide transparency and immediate feedback to the trader, preventing UI freezes.

## 3. Database Design
N/A

## 4. API / Frontend Design
- **Component**: `ChatWidget.tsx` integrated into the `Dashboard.tsx`.
- **State Management**: A React array holding `Message` objects.
  - Roles: `user` | `assistant`
  - A message can have an active `tool` state to show a loading badge.
- **WebSocket**: Connect to `ws://localhost:8000/api/v1/ws/chat?token=<jwt>`.

## 5. Architecture Decisions
- Parse incoming JSON chunks from the server:
  - `type: token`: Append text to the latest assistant message.
  - `type: tool_start`: Display a "Working on: <tool_name>" badge on the latest assistant message.
  - `type: tool_end`: Remove or gray out the badge.
  - `type: message_end`: Mark the stream as finished, re-enable the user input field.
- The UI must auto-scroll to the bottom when new tokens arrive.

## 6. Commit Sequence
1. `chore: add milestone 13 plan`
2. `feat(frontend): create ChatWidget UI and message state`
3. `feat(frontend): integrate WebSocket connection for streaming chunks`
4. `docs(frontend): update Developer Guide and changelog`
