import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_portfolio_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/portfolio")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_submit_order_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/orders", json={
            "symbol": "AAPL",
            "order_type": "MARKET",
            "side": "BUY",
            "quantity": 10.0
        })
    assert response.status_code == 401
