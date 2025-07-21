# backend/database.py
import sqlite3
from contextlib import contextmanager

# Use a temporary, in-memory database for testing, and a file for production
DATABASE_URL = "tasks.db"

@contextmanager
def get_db_connection(db_url=DATABASE_URL):
    """Context manager for database connections."""
    conn = sqlite3.connect(db_url)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db(db_url=DATABASE_URL):
    """Initializes the database table."""
    with get_db_connection(db_url) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.commit()