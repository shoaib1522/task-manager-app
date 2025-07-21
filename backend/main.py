# backend/main.py

# --- FIX: Change relative import to absolute import ---
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List
import sqlite3
# This now works because Python sees 'backend' as a top-level package.
from backend.database import init_db, get_db_connection

init_db()

app = FastAPI()

# ... (rest of the file is the same)
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

@app.get("/tasks", response_model=List[Task])
def get_tasks(conn: sqlite3.Connection = Depends(get_db_connection)):
    tasks = conn.execute("SELECT id, title, completed FROM tasks").fetchall()
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, task.completed),
    )
    conn.commit()
    new_task_id = cursor.lastrowid
    return {"id": new_task_id, **task.dict()}