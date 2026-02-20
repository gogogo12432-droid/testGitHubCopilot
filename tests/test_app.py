import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball Team" in data
    assert isinstance(data["Basketball Team"]["participants"], list)

def test_signup_success():
    response = client.post("/activities/Basketball%20Team/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Basketball%20Team/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Basketball%20Team/signup?email=unregister@example.com")
    # Then unregister
    response = client.post("/activities/Basketball%20Team/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]

def test_unregister_not_signed_up():
    response = client.post("/activities/Basketball%20Team/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]

def test_unregister_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]