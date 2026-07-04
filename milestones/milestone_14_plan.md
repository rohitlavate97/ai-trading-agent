# Milestone 14: Trading UI & Portfolio Widgets

## 1. Business Requirement
While conversational AI is powerful, traders require high-density visual data. We need dedicated UI components to display real-time balances, open positions, and historical order data.

## 2. Trading/Financial Workflow
The dashboard must act as a command center. A split view will allow users to converse with the AI on one side while monitoring their live portfolio state and execution history on the other.

## 3. Database Design
N/A

## 4. API / Frontend Design
- **Components**: 
  - `PortfolioWidget.tsx`: Fetches `GET /api/v1/portfolio` to render cash balance, total equity, and a data table of `Position` objects.
  - `OrderHistoryWidget.tsx`: Fetches `GET /api/v1/orders` to render a data table of `Order` objects.
- **Layout**: Update `Dashboard.tsx` and `Dashboard.css` to use a responsive CSS Grid, placing widgets alongside the `ChatWidget`.

## 5. Architecture Decisions
- React `useEffect` hooks will trigger API calls on mount.
- In a future milestone, these could subscribe to WebSocket broadcasts for live updates, but standard REST polling/mounting is sufficient for now.
- Tables will reuse the vanilla CSS glassmorphic aesthetic defined in `index.css`.

## 6. Commit Sequence
1. `chore: add milestone 14 plan`
2. `feat(frontend): create PortfolioWidget and OrderHistory components`
3. `feat(frontend): update Dashboard layout to integrate widgets`
4. `docs(frontend): update Developer Guide and changelog`
