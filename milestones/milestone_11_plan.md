# Milestone 11: Frontend layout and routing setup

## 1. Business Requirement
The backend is stable and highly capable. Now, we must lay the foundation for a premium, interactive user interface. The UI must facilitate seamless navigation between authentication screens and the primary trading dashboard.

## 2. Trading/Financial Workflow
A centralized layout enables users to fluidly switch contexts (e.g., viewing a chart, chatting with the AI, executing a trade) without full-page reloads, mirroring professional trading terminals.

## 3. Database Design
N/A

## 4. API / Frontend Design
- **Tech Stack**: React + TypeScript powered by Vite.
- **Routing**: `react-router-dom` for handling routes:
  - `/login` (Public)
  - `/register` (Public)
  - `/` (Private Dashboard: Chat + Widgets)
- **Styling**: Vanilla CSS utilizing modern CSS variables and a premium, glassmorphic design system to create a "wow" factor, avoiding generic styling frameworks as per constraints.

## 5. Architecture Decisions
- Create a `frontend` directory in the project root.
- Initialize using `create-vite`.
- Establish global design tokens (colors, fonts, shadows) in `index.css`.
- Create a layout component (`AuthLayout` and `DashboardLayout`) to wrap routes.

## 6. Commit Sequence
1. `chore(frontend): initialize Vite + React + TS project`
2. `feat(frontend): setup global CSS design tokens and aesthetic foundation`
3. `feat(frontend): setup React Router with layout components`
4. `docs(frontend): update Developer Guide and changelog`
