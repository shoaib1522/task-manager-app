# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import sqlite3
from .database import init_db, get_db_connection

# Initialize the database on startup
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
    tasks = conn.execute("SELECT id, title, completed FROM tasks").fetchall()
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (task.title, task.completed))
    conn.commit()
    new_task_id = cursor.lastrowid
    return {"id": new_task_id, **task.dict()}