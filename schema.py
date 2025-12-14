"""Simple SQLite schema helpers for Vehicle/Car models.

This module provides small helpers to create SQLite tables that mirror the
Vehicle/Car classes used in `models/vehicle.py`. It's intentionally small
so you can use it for local testing.
"""

import sqlite3
from typing import Optional


def create_connection(db_path: str) -> sqlite3.Connection:
	"""Create and return a sqlite3 connection to db_path."""
	conn = sqlite3.connect(db_path)
	return conn


def create_tables(conn: sqlite3.Connection) -> None:
	"""Create tables for vehicles and cars.

	The `vehicles` table stores generic vehicle rows. For cars we store
	number of doors as an optional column (NULL for non-car vehicles).
	"""
	cur = conn.cursor()
	cur.execute(
		"""
		CREATE TABLE IF NOT EXISTS vehicles (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			make TEXT NOT NULL,
			model TEXT NOT NULL,
			year INTEGER NOT NULL,
			fuel_type TEXT NOT NULL,
			num_doors INTEGER
		);
		"""
	)
	conn.commit()


def drop_tables(conn: sqlite3.Connection) -> None:
	cur = conn.cursor()
	cur.execute("DROP TABLE IF EXISTS vehicles;")
	conn.commit()


if __name__ == "__main__":
	# Quick local smoke-test
	conn = create_connection(":memory:")
	create_tables(conn)
	print("Created in-memory schema for vehicles.")

