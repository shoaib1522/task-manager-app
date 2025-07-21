# backend/database.py

import sqlite3

# FIX: Remove the import of contextmanager
# from contextlib import contextmanager

DATABASE_URL = "tasks.db"


# FIX: Remove the @contextmanager decorator.
# This function is now a "dependency with yield," which is the correct FastAPI pattern.
def get_db_connection(db_url=DATABASE_URL):
    """Dependency to get a database connection that is closed after the request."""
    conn = sqlite3.connect(db_url)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_url=DATABASE_URL):
    """Initializes the database table."""
    # Use our dependency directly to ensure proper connection handling.
    # Note: This is a slight change to use the with statement here for initialization.
    with sqlite3.connect(db_url) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """
        )
        conn.commit()
