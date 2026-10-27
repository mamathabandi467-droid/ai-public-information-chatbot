
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_empty_chat_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200
    assert response.json()["reply"] == "Please enter your question."


def test_chat_without_message():
    response = client.post("/chat", json={})
    assert response.status_code == 422
