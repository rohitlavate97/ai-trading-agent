# Production Readiness Guide

While we have built a highly sophisticated and modern architectural foundation (FastAPI, React, LangGraph, WebSockets, JWT, SQLAlchemy), **the current application is an MVP (Minimum Viable Product) and is NOT 100% production-ready or industry-grade for real financial transactions.**

To elevate this application from a powerful prototype to an industry-grade, production-ready trading platform, several critical layers must be implemented. Below is a comprehensive guide on what needs to be added, along with practical implementation examples.

---

## 1. Real Financial Data & Execution Engines
Right now, the app uses mocked data and instantaneous, simulated market executions.

### Live Market Data (Example: Polygon.io)
You must swap the `get_stock_price` tool to call a real financial API.

**Implementation Example (`backend/agents/tools.py`):**
```python
import httpx
from core.config import settings

@tool
async def get_stock_price(symbol: str) -> dict:
    """Fetch real-time stock price from Polygon.io"""
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={settings.POLYGON_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if data.get("resultsCount", 0) > 0:
            return {"symbol": symbol, "price": data["results"][0]["c"], "currency": "USD"}
        return {"error": "Symbol not found"}
```

### Brokerage API Integration (Example: Alpaca)
Instead of just updating the local MySQL balance, actual trades must be routed to a clearinghouse.

**Implementation Example (`backend/services/portfolio_service.py`):**
```python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Initialize Alpaca Paper Trading client
trading_client = TradingClient('api-key', 'secret-key', paper=True)

async def execute_trade(user, symbol, quantity, side):
    # 1. Route to Alpaca
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=quantity,
        side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )
    alpaca_order = trading_client.submit_order(order_data=market_order_data)
    
    # 2. Update local DB to reflect "PENDING" status until Alpaca confirms fill via Webhook
    return {"status": alpaca_order.status, "id": alpaca_order.id}
```

---

## 2. Security & Compliance (Critical)
Handling user funds requires bank-level security.

### Secrets Management
Never store API keys in raw `.env` files in production. Use a cloud secrets manager (e.g., AWS Secrets Manager).

**Implementation Example (`backend/core/config.py`):**
```python
import boto3
from pydantic_settings import BaseSettings

def get_secret(secret_name: str) -> str:
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

class Settings(BaseSettings):
    # Fetch at runtime instead of relying on local OS env vars
    DATABASE_URL: str = get_secret("prod/db_url")
    OPENAI_API_KEY: str = get_secret("prod/openai_key")
```

---

## 3. Infrastructure & Scalability
Local development using `uvicorn` and SQLite/Local MySQL will not scale to thousands of active concurrent traders.

### Docker Containerization
You must package the backend into a Docker image for deployment to Kubernetes or AWS ECS.

**Implementation Example (`backend/Dockerfile`):**
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run uvicorn with multiple workers for concurrency in production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Redis WebSocket Broadcaster
FastAPI websockets currently live in server memory. If you scale to 5 servers, Server A cannot broadcast a message to a user connected to Server B. You must use Redis Pub/Sub.

**Implementation Example (`backend/api/routers/websockets.py`):**
```python
import redis.asyncio as redis

redis_client = redis.Redis.from_url("redis://redis-cluster:6379")

async def broadcast_to_user(user_id: str, message: str):
    # Publish message to a central Redis channel instead of local memory array
    await redis_client.publish(f"user_stream_{user_id}", message)
```

---

## 4. Advanced AI & RAG Pipeline
- **Continuous Ingestion Pipeline**: Build automated Celery tasks to constantly scrape, embed, and ingest real-time news and SEC filings into Qdrant.
- **Guardrails**: Implement strict prompt-injection protections to ensure the AI *never* executes a trade without explicit human confirmation.

**Implementation Example (Human-in-the-Loop LangGraph):**
```python
# In backend/agents/supervisor.py
from langgraph.checkpoint.sqlite import SqliteSaver

# Add a breakpoint before the portfolio agent executes a trade
workflow.add_node("execute_trade", execute_trade_tool)
workflow.add_edge("portfolio_agent", "execute_trade")

# Compile with a persistent checkpointer and an interrupt
memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["execute_trade"] # Pauses the graph and waits for user approval
)
```

---

## 5. Testing & Observability
- **Observability**: Integrate Datadog or Prometheus.

**Implementation Example (FastAPI Prometheus Middleware):**
```python
from prometheus_fastapi_instrumentator import Instrumentator
from main import app

# Automatically exposes a /metrics endpoint for Grafana to scrape API latencies
Instrumentator().instrument(app).expose(app)
```
