"""Script to recreate and seed the persistent dev database."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.seed_data import seed_file


def main():
    db_path = "data/dev.db"
    seed_file(db_path, overwrite=True)
    print(f"Reset and seeded database at {db_path}")


if __name__ == "__main__":
    main()
