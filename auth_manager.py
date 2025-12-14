import bcrypt
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager


class PasswordHasher:
    """Utility class for hashing and verifying passwords using bcrypt."""

    @staticmethod
    def hash(plain_password: str) -> str:
        hashed_bytes = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )


class AuthenticationService:
    """Service responsible for user registration and authentication."""

    def __init__(self, database: DatabaseManager):
        self._database = database
        self._hasher = PasswordHasher()

    def register_user(
        self,
        username: str,
        password: str,
        role: str = "user"
    ):
        """Register a new user if the username is not already taken."""
        user_exists = self._database.fetch_one(
            "SELECT username FROM users WHERE username = ?",
            (username,),
        )

        if user_exists:
            return False, "Username already exists."

        password_hash = self._hasher.hash(password)
        self._database.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )

        return True, "User registered successfully."

    def authenticate_user(
        self,
        username: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user credentials and return a User object on success."""
        record = self._database.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )

        if record is None:
            return None

        db_username, db_password_hash, db_role = record

        if self._hasher.verify(password, db_password_hash):
            return User(db_username, db_password_hash, db_role)

        return None
