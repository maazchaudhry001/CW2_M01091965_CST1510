# app/data/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row   # <-- return row objects that convert to dicts
    return conn
