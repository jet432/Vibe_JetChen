from models.entities import Account, Transaction
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository


class AccountService:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def createAccount(self, userId: int, accountType: str) -> Account:
        return self.account_repository.create(user_id=userId, account_type=accountType)

    def getAccount(self, accountId: str) -> Account | None:
        return self.account_repository.get(accountId)

    def deposit(self, accountId: str, amount: float) -> Account:
        account = self.account_repository.get(accountId)
        if account is None:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        account.balance += amount
        self.account_repository.save(account)
        self.transaction_repository.add(
            Transaction(account_id=accountId, tx_type="DEPOSIT", amount=amount)
        )
        return account

    def withdraw(self, accountId: str, amount: float) -> Account:
        account = self.account_repository.get(accountId)
        if account is None:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if account.balance < amount:
            raise ValueError("Insufficient funds")
        account.balance -= amount
        self.account_repository.save(account)
        self.transaction_repository.add(
            Transaction(account_id=accountId, tx_type="WITHDRAW", amount=amount)
        )
        return account

    def getTransactions(self, accountId: str) -> list[Transaction]:
        account = self.account_repository.get(accountId)
        if account is None:
            raise ValueError("Account not found")
        return self.transaction_repository.get_for_account(accountId)

