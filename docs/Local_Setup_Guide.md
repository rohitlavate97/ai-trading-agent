# Local Development Setup Guide

## Prerequisites
- Python 3.13+
- Node.js (for Angular)
- Docker Desktop (or equivalent docker engine)

## Setting up the Environment
1. Clone the repository.
2. Copy `.env.example` to `.env` and fill out your local credentials and API keys.
3. Start the infrastructure via Docker Compose:
   ```bash
   docker compose up -d
   ```
4. Install backend dependencies:
   ```bash
   cd backend
   pip install -e .
   ```
5. Run database migrations and seed data:
   ```bash
   cd backend
   alembic upgrade head
   python db/seed.py
   ```
6. Run the backend server locally:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## Pre-commit Hooks
Run `pre-commit install` in the root of the repository to set up the hooks.
