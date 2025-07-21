# backend/test_main.py
import pytest
import sqlite3
from fastapi.testclient import TestClient

# --- FIX: Change relative imports to absolute imports ---
from backend.main import app, get_db_connection
from backend.database import init_db

TEST_DB_URL = "file:memdb1?mode=memory&cache=shared"


def get_test_db_connection():
    conn = sqlite3.connect(TEST_DB_URL, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


app.dependency_overrides[get_db_connection] = get_test_db_connection


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    conn = get_test_db_connection()
    init_db(db_url=TEST_DB_URL)
    yield
    conn.close()


client = TestClient(app)


def test_create_and_get_tasks():
    response = client.post("/tasks", json={"title": "Test Task", "completed": False})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] is not None

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"
