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
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    assert response.json()["completed"] is False

def test_read_todos(client):
    client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False})
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == "Test Todo"

def test_update_todo(client):
    # Create a todo first
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False})
    todo_id = response.json()["id"]
    # Update it
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated Todo", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"
    assert response.json()["completed"] is True

def test_delete_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test", "completed": False})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted"
    # Verify deletion
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404