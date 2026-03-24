from models.entities import Transaction


class TransactionRepository:
    def __init__(self) -> None:
        self._transactions: dict[str, list[Transaction]] = {
            "1": [Transaction(account_id="1", tx_type="DEPOSIT", amount=500.0)],
            "2": [Transaction(account_id="2", tx_type="DEPOSIT", amount=1200.0)],
            "3": [Transaction(account_id="3", tx_type="DEPOSIT", amount=3000.0)],
        }

    def add(self, transaction: Transaction) -> None:
        if transaction.account_id not in self._transactions:
            self._transactions[transaction.account_id] = []
        self._transactions[transaction.account_id].append(transaction)

    def get_for_account(self, account_id: str) -> list[Transaction]:
        return self._transactions.get(account_id, [])

