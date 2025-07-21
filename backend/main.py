# backend/main.py

from fastapi import FastAPI, Depends

# FIX: Import the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import sqlite3
from backend.database import init_db, get_db_connection

init_db()

app = FastAPI()

# --- THIS IS THE FIX ---
# Define the list of "origins" (addresses) that are allowed to talk to our API.
# For local development, this is our React app's address.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add the CORSMiddleware to our application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# -----------------------


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int


@app.get("/tasks", response_model=List[Task])
def get_tasks(conn: sqlite3.Connection = Depends(get_db_connection)):
    rows = conn.execute("SELECT id, title, completed FROM tasks").fetchall()
    tasks = [dict(row) for row in rows]
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(
    task: TaskCreate, conn: sqlite3.Connection = Depends(get_db_connection)
):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, task.completed),
    )
    conn.commit()
    new_task_id = cursor.lastrowid
    return {"id": new_task_id, **task.model_dump()}
