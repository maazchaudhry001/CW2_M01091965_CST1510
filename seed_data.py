"""Seed data helpers for the simple vehicles schema.

This module provides a small seed routine that inserts example vehicle rows
into the `vehicles` table created by `database.schema.create_tables`. It also
provides a convenience function to seed a persistent database file.
"""

import os
import argparse
from .schema import create_tables, create_connection


def seed(conn):
	cur = conn.cursor()
	sample = [
		("GenericMake", "ModelX", 2018, "hybrid", None),
		("Audi", "A3", 2020, "petrol", 4),
		("Tesla", "Model 3", 2023, "electric", 4),
	]
	cur.executemany(
		"INSERT INTO vehicles (make, model, year, fuel_type, num_doors) VALUES (?, ?, ?, ?, ?);",
		sample,
	)
	conn.commit()


def seed_file(db_path: str = "data/dev.db", overwrite: bool = False) -> str:
	"""Seed a database file at `db_path`. If overwrite is True the file is removed first.

	Returns the path to the database file.
	"""
	db_dir = os.path.dirname(db_path)
	if db_dir and not os.path.exists(db_dir):
		os.makedirs(db_dir, exist_ok=True)

	if overwrite and os.path.exists(db_path):
		os.remove(db_path)

	conn = create_connection(db_path)
	create_tables(conn)
	seed(conn)
	conn.close()
	return db_path


def _parse_args():
	parser = argparse.ArgumentParser(description="Seed the vehicles database.")
	parser.add_argument("--db", default="data/dev.db", help="Path to the sqlite DB file")
	parser.add_argument("--overwrite", action="store_true", help="Overwrite existing DB file")
	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	path = seed_file(args.db, overwrite=args.overwrite)
	print(f"Seeded database at: {path}")

