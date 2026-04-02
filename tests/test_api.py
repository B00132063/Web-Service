from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_get_all():
    response = client.get("/getAll")
    assert response.status_code == 200
    assert isinstance(response.json(), list)