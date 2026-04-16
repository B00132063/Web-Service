# Import FastAPI's testing client so we can send fake requests to our API
from fastapi.testclient import TestClient
# Imports the FastAPI app we created in main.py so we can test it
from app.main import app

# Create a test client linked to the FastAPI app
client = TestClient(app)

# Test the home route to make sure the API is running
def test_home():
    # Send a GET request to the home route
    response = client.get("/")
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

# Test the getAll route to make sure it returns a list of products
def test_get_all():
    # Send a GET request to the getAll route
    response = client.get("/getAll")
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the response is a list (of products)
    assert isinstance(response.json(), list)