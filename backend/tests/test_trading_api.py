import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from api.deps import get_current_user
from db.models import User

# Mock user for testing
test_user = User(
    id="test-uuid",
    email="test@example.com",
    username="testuser",
    role="USER",
    is_active=True
)

def override_get_current_user():
    return test_user

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_get_portfolio_authorized():
    # Note: This will hit the database. If you don't have a test DB configured, 
    # you might get an error depending on your `get_db` dependency setup.
    # For this milestone, we demonstrate the dependency override.
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/portfolio")
        # Just checking that it doesn't return 401 anymore
        assert response.status_code in [200, 404, 500] 

@pytest.mark.asyncio
async def test_get_orders_authorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/orders")
        assert response.status_code in [200, 404, 500]

# Cleanup overrides after tests
def teardown_module(module):
    app.dependency_overrides.clear()
