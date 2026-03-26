from models.entities import Transaction
from database import SessionLocal
from models.sql_models import TransactionModel


class TransactionRepository:
    def __init__(self) -> None:
        pass

    def add(self, transaction: Transaction) -> None:
        if not transaction.account_id.isdigit():
            return
        with SessionLocal() as db:
            row = TransactionModel(
                account_id=int(transaction.account_id),
                txn_type=transaction.tx_type,
                amount=transaction.amount,
            )
            db.add(row)
            db.commit()

    def get_for_account(self, account_id: str) -> list[Transaction]:
        if not account_id.isdigit():
            return []
        with SessionLocal() as db:
            rows = (
                db.query(TransactionModel)
                .filter(TransactionModel.account_id == int(account_id))
                .order_by(TransactionModel.txn_id.asc())
                .all()
            )

            return [
                Transaction(
                    account_id=str(row.account_id),
                    tx_type=row.txn_type,
                    amount=float(row.amount),
                    timestamp=row.created_at.isoformat() if row.created_at else "",
                    txn_id=row.txn_id,
                )
                for row in rows
            ]
