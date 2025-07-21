# backend/main.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List
import sqlite3
from backend.database import init_db, get_db_connection

init_db()

app = FastAPI()


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int


@app.get("/tasks", response_model=List[Task])
def get_tasks(conn: sqlite3.Connection = Depends(get_db_connection)):
    # --- THIS IS THE FIX ---
    # Fetch the rows from the database
    rows = conn.execute("SELECT id, title, completed FROM tasks").fetchall()
    # Convert each sqlite3.Row object into a standard Python dictionary
    tasks = [dict(row) for row in rows]
    return tasks
    # -----------------------


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
    # Use model_dump() which is the modern Pydantic V2 way, to resolve the warning.
    return {"id": new_task_id, **task.model_dump()}
