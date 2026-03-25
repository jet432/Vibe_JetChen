from models.entities import Account
from database import SessionLocal
from models.sql_models import AccountModel


class AccountRepository:
    def __init__(self) -> None:
        pass

    def create(self, user_id: int, account_type: str) -> Account:
        with SessionLocal() as db:
            row = AccountModel(user_id=user_id, account_type=account_type, balance=0.0)
            db.add(row)
            db.commit()
            db.refresh(row)
            return Account(
                account_id=str(row.account_id),
                user_id=row.user_id,
                account_type=row.account_type,
                balance=float(row.balance),
            )

    def get(self, account_id: str) -> Account | None:
        if not account_id.isdigit():
            return None
        with SessionLocal() as db:
            row = db.query(AccountModel).filter(AccountModel.account_id == int(account_id)).first()
            if row is None:
                return None
            return Account(
                account_id=str(row.account_id),
                user_id=row.user_id,
                account_type=row.account_type,
                balance=float(row.balance),
            )

    def save(self, account: Account) -> None:
        if not account.account_id.isdigit():
            return
        with SessionLocal() as db:
            row = db.query(AccountModel).filter(AccountModel.account_id == int(account.account_id)).first()
            if row is None:
                return
            row.user_id = account.user_id
            row.account_type = account.account_type
            row.balance = account.balance
            db.commit()
