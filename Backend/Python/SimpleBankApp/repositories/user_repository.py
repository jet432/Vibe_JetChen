from models.entities import User


class UserRepository:
    def __init__(self) -> None:
        self._users_by_name: dict[str, User] = {
            "alice": User(user_id=1, username="alice", password="password123"),
            "bob": User(user_id=2, username="bob", password="securepass"),
        }

    def get_by_username(self, username: str) -> User | None:
        return self._users_by_name.get(username)

    def add(self, username: str, password: str) -> User:
        next_id = len(self._users_by_name) + 1
        user = User(user_id=next_id, username=username, password=password)
        self._users_by_name[username] = user
        return user

