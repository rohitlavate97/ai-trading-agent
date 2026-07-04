import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from schemas.watchlist import WatchlistCreate, WatchlistItemCreate

@pytest.mark.asyncio
async def test_create_watchlist_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/watchlists", json={"name": "Tech Stocks", "description": "My tech stocks"})
    assert response.status_code == 401
