from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_category():
    response = client.post("/api/v1/categories/", json={"name": "Electronics"})
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"


def test_read_categories():
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_category():
    response = client.get("/api/v1/categories/1")
    assert response.status_code == 200
    assert "name" in response.json()
