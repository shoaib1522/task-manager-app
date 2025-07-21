# backend/test_main.py
import pytest
import sqlite3
from fastapi.testclient import TestClient
from .main import app, get_db_connection
from .database import init_db


# Use an in-memory SQLite database for testing
TEST_DB_URL = "file:memdb1?mode=memory&cache=shared"


# Override the dependency to use the in-memory database for tests
def get_test_db_connection():
    # 'uri=True' is needed for shared in-memory DB
    conn = sqlite3.connect(TEST_DB_URL, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


app.dependency_overrides[get_db_connection] = get_test_db_connection


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture to set up and tear down the database for each test."""
    conn = get_test_db_connection()
    init_db(db_url=TEST_DB_URL)
    yield
    conn.close()


client = TestClient(app)


def test_create_and_get_tasks():
    # 1. Create a task
    response = client.post("/tasks", json={"title": "Test Task", "completed": False})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] is not None

    # 2. Get all tasks and verify the new task is there
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"


# FIX: Ensure there is a blank line after this line in your editor.
