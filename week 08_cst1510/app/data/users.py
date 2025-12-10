# app/data/users.py
from pathlib import Path
import sqlite3

# import the shared DB connector (adjust path if using a single-file main)
try:
    from app.data.db import connect_database
except Exception:
    # Fallback if you run the single-file main.py which defines connect_database
    # (this keeps compatibility while you test)
    def connect_database(db_path=Path("DATA") / "intelligence_platform.db"):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(db_path))


def get_user_by_username(username):
    """Return the user row (tuple) or None if not found."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(username, password_hash, role='user'):
    """Insert a new user. Raises sqlite3.IntegrityError if username exists."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()


# Compatibility aliases expected by other modules
def find_user(username):
    """Alias for get_user_by_username to satisfy imports elsewhere."""
    return get_user_by_username(username)
