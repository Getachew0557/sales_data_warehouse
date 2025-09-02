import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal, engine
from src import models

@pytest.fixture
def client():
    models.Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False, "user_id": 1, "category": "Test"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_read_todos(client):
    client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False, "user_id": 1, "category": "Test"})
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) >= 1