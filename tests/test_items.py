import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={
        "name": "Test Item",
        "email": "test@example.com",
        "item_name": "Test Item Name",
        "quantity": 10,
        "expiry_date": "31-12-2024"
    })
    assert response.status_code == 200
    assert "id" in response.json()
