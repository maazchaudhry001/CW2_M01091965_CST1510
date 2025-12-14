"""Small script that creates schema, seeds data, loads model instances and prints them.

This script adjusts sys.path so it can be executed directly from the project root
and still import the local `database` and `models` packages.
"""

import os
import sys

# Ensure project root (parent of scripts/) is on sys.path so sibling packages
# (database, models) can be imported when this script runs directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.schema import create_connection, create_tables
from database.seed_data import seed
from database.loader import load_vehicles


def main():
    conn = create_connection(":memory:")
    create_tables(conn)
    seed(conn)
    vehicles = load_vehicles(conn)
    for v in vehicles:
        print(f"{type(v).__name__}: {v}")


if __name__ == "__main__":
    main()
