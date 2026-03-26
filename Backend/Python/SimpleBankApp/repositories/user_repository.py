from database import get_db, get_next_sequence
from models.entities import User


class UserRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _collection():
        return get_db().users

    @staticmethod
    def _to_entity(row: dict) -> User:
        return User(
            user_id=int(row.get("user_id", 0)),
            username=row.get("name", ""),
            email=row.get("email", ""),
            password=row.get("password", ""),
        )

    def get_by_id(self, user_id: int) -> User | None:
        row = self._collection().find_one({"user_id": int(user_id)})
        if row is None:
            return None
        return self._to_entity(row)

    def get_by_username(self, username: str) -> User | None:
        row = self._collection().find_one({"name": username})
        if row is None:
            return None
        return self._to_entity(row)

    def get_by_email(self, email: str) -> User | None:
        row = self._collection().find_one({"email": email})
        if row is None:
            return None
        return self._to_entity(row)

    def add(self, username: str, email: str, password: str) -> User:
        user_id = get_next_sequence("users")
        payload = {
            "user_id": user_id,
            "name": username,
            "email": email,
            "password": password,
        }
        self._collection().insert_one(payload)
        return self._to_entity(payload)

    def update_password(self, user_id: int, password: str) -> None:
        self._collection().update_one(
            {"user_id": int(user_id)},
            {"$set": {"password": password}},
        )