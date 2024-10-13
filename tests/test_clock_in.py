import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_clock_in():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/clock-in/clock-in/", json={
            "email": "test@gmail.com",
            "location": "LOC"
        })
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"

@pytest.mark.asyncio
async def test_filter_clock_in():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/clock-in/clock-in/filter", params={"email": "test@gmail.com"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
