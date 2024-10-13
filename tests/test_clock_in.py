import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_clock_in():
    response = client.post("/clock-in/", json={
        "email": "test@example.com",
        "location": "XYZ"
    })
    assert response.status_code == 200
    assert "id" in response.json()
