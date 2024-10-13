import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items/items/", json={
            "name": "Test Item",
            "email": "test@gmail.com",
            "item_name": "Test Item Name",
            "quantity": 10,
            "expiry_date": "15-10-2024"
        })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

@pytest.mark.asyncio
async def test_filter_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/items/filter", params={"email": "test@gmail.com"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
