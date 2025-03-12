from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_store():
    response = client.post("/api/v1/stores/", json={"name": "SuperStore", "address": "123 Main St", "city": "New York"})
    assert response.status_code == 200
    assert response.json()["name"] == "SuperStore"
    assert response.json()["city"] == "New York"


def test_read_stores():
    response = client.get("/api/v1/stores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_store():
    response = client.get("/api/v1/stores/1")
    assert response.status_code == 200
    assert "city" in response.json()
    