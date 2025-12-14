import sqlite3
from pathlib import Path

# Ensure data folder exists
Path("data").mkdir(exist_ok=True)

conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Database initialized and users table created.")
