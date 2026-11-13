
from fastapi.testclient import TestClient
from app.api.routes import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "AI Research Agent API is running!"
    }

def test_api_documentation():
    response = client.get("/docs")

    assert response.status_code == 200


def test_invalid_route():
    response = client.get("/invalid")

    assert response.status_code == 404
