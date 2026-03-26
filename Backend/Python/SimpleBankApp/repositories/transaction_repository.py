from datetime import datetime, timezone

from database import get_db, get_next_sequence
from models.entities import Transaction


class TransactionRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _collection():
        return get_db().transactions

    @staticmethod
    def _to_entity(row: dict) -> Transaction:
        return Transaction(
            account_id=str(row.get("account_id", "")),
            tx_type=row.get("txn_type", ""),
            amount=float(row.get("amount", 0.0)),
            timestamp=row.get("created_at", ""),
            txn_id=int(row["txn_id"]) if row.get("txn_id") is not None else None,
        )

    def add(self, transaction: Transaction) -> None:
        if not transaction.account_id.isdigit():
            return

        payload = {
            "txn_id": get_next_sequence("transactions"),
            "account_id": int(transaction.account_id),
            "txn_type": transaction.tx_type,
            "amount": float(transaction.amount),
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        self._collection().insert_one(payload)

    def get_for_account(self, account_id: str) -> list[Transaction]:
        if not account_id.isdigit():
            return []

        rows = self._collection().find({"account_id": int(account_id)}).sort("txn_id", 1)
        return [self._to_entity(row) for row in rows]