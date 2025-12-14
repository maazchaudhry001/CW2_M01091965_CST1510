import sqlite3
from typing import Any, Iterable
from pathlib import Path


class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str | Path = Path("data") / "dev.db"):
        # Default to a seeded dev DB inside the project's `data/` folder.
        self._db_path = str(db_path)   # ensure sqlite gets a string path
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        """Open a database connection if not already connected."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: Iterable[Any] = ()):
        """Execute INSERT / UPDATE / DELETE queries."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur

    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        """Fetch a single row."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        """Fetch all rows."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()
