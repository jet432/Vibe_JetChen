from database import get_db, get_next_sequence
from models.entities import Account


class AccountRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _collection():
        return get_db().accounts

    @staticmethod
    def _to_entity(row: dict) -> Account:
        return Account(
            account_id=str(row.get("account_id", "")),
            user_id=int(row.get("user_id", 0)),
            account_type=row.get("account_type", ""),
            balance=float(row.get("balance", 0.0)),
        )

    def create(self, user_id: int, account_type: str) -> Account:
        account_id = get_next_sequence("accounts")
        payload = {
            "account_id": account_id,
            "user_id": int(user_id),
            "account_type": account_type,
            "balance": 0.0,
        }
        self._collection().insert_one(payload)
        return self._to_entity(payload)

    def get(self, account_id: str) -> Account | None:
        if not account_id.isdigit():
            return None

        row = self._collection().find_one({"account_id": int(account_id)})
        if row is None:
            return None
        return self._to_entity(row)

    def save(self, account: Account) -> None:
        if not account.account_id.isdigit():
            return

        self._collection().update_one(
            {"account_id": int(account.account_id)},
            {
                "$set": {
                    "user_id": int(account.user_id),
                    "account_type": account.account_type,
                    "balance": float(account.balance),
                }
            },
        )

    def get_for_user(self, user_id: int) -> list[Account]:
        rows = self._collection().find({"user_id": int(user_id)}).sort("account_id", 1)
        return [self._to_entity(row) for row in rows]