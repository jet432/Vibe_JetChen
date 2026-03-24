from models.entities import Account


class AccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {
            "1": Account(account_id="1", user_id=1, account_type="SAVINGS", balance=500.0),
            "2": Account(account_id="2", user_id=2, account_type="CHECKING", balance=1200.0),
            "3": Account(account_id="3", user_id=3, account_type="BUSINESS", balance=3000.0),
        }
        self._next_id = 4

    def create(self, user_id: int, account_type: str) -> Account:
        account_id = str(self._next_id)
        self._next_id += 1
        account = Account(
            account_id=account_id,
            user_id=user_id,
            account_type=account_type,
            balance=0.0,
        )
        self._accounts[account_id] = account
        return account

    def get(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def save(self, account: Account) -> None:
        self._accounts[account.account_id] = account

