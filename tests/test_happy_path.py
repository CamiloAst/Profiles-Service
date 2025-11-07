import json
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "UP"

def test_happy_path_crud():
    # Create/Upsert
    payload = {
        "nickname": "cami",
        "bio": "Hola mundo",
        "country": "CO",
        "social_links": {"x": "https://x.com/cami"}
    }
    r = client.post("/profiles", params={"user_id":"u123"}, json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["user_id"] == "u123"
    assert body["nickname"] == "cami"
    assert body["social_links"]["x"].startswith("https://")

    # Get
    r = client.get("/profiles/u123")
    assert r.status_code == 200
    assert r.json()["bio"] == "Hola mundo"

    # Update
    r = client.put("/profiles/u123", json={"bio":"Actualizada"})
    assert r.status_code == 200
    assert r.json()["bio"] == "Actualizada"

    # Delete
    r = client.delete("/profiles/u123")
    assert r.status_code == 204

    # Confirm 404
    r = client.get("/profiles/u123")
    assert r.status_code == 404
