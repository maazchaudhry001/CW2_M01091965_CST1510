"""Integration smoke test for AuthenticationService using the seeded dev DB.

This script will ensure the users table exists in `data/dev.db`, then try to
register and authenticate a user using `services.auth_manager.AuthenticationService`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.database_manager import DatabaseManager
from services.auth_manager import AuthenticationService
from database.seed_data import seed_file


def ensure_users_table(db: DatabaseManager):
    db.connect()
    db.execute_query(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )


def main():
    # Ensure dev DB is present and seeded (won't overwrite by default)
    seed_file("data/dev.db", overwrite=False)

    db = DatabaseManager()  # defaults to data/dev.db
    ensure_users_table(db)

    auth = AuthenticationService(db)

    username = "alice"
    password = "password123"

    print(f"Registering user '{username}'...")
    success, message = auth.register_user(username, password, role="admin")
    print("Register result:", success, message)

    print(f"Authenticating '{username}' with correct password...")
    user = auth.authenticate_user(username, password)
    print("Authenticated user object:", user)

    print(f"Authenticating '{username}' with wrong password...")
    bad = auth.authenticate_user(username, "wrongpass")
    print("Result for wrong password:", bad)

    # cleanup connection
    db.close()


if __name__ == "__main__":
    main()
