from models.entities import User
from database import SessionLocal
from models.sql_models import UserModel


class UserRepository:
    def __init__(self) -> None:
        pass

    def get_by_id(self, user_id: int) -> User | None:
        with SessionLocal() as db:
            row = db.query(UserModel).filter(UserModel.user_id == user_id).first()
            if row is None:
                return None
            return User(
                user_id=row.user_id,
                username=row.name,
                email=row.email or "",
                password=row.password or "",
            )

    def get_by_username(self, username: str) -> User | None:
        with SessionLocal() as db:
            row = db.query(UserModel).filter(UserModel.name == username).first()
            if row is None:
                return None
            return User(
                user_id=row.user_id,
                username=row.name,
                email=row.email or "",
                password=row.password or "",
            )

    def get_by_email(self, email: str) -> User | None:
        with SessionLocal() as db:
            row = db.query(UserModel).filter(UserModel.email == email).first()
            if row is None:
                return None
            return User(
                user_id=row.user_id,
                username=row.name,
                email=row.email or "",
                password=row.password or "",
            )

    def add(self, username: str, email: str, password: str) -> User:
        with SessionLocal() as db:
            row = UserModel(
                name=username,
                email=email,
                password=password,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return User(
                user_id=row.user_id,
                username=row.name,
                email=row.email or "",
                password=row.password or "",
            )

    def update_password(self, user_id: int, password: str) -> None:
        with SessionLocal() as db:
            row = db.query(UserModel).filter(UserModel.user_id == user_id).first()
            if row is None:
                return
            row.password = password
            db.commit()
