from models.entities import Account, Transaction, User


def user_to_dict(user: User) -> dict:
    return {"userId": user.user_id, "username": user.username}


def account_to_dict(account: Account) -> dict:
    return {
        "accountId": account.account_id,
        "userId": account.user_id,
        "accountType": account.account_type,
        "balance": account.balance,
    }


def transaction_to_dict(transaction: Transaction) -> dict:
    return {
        "accountId": transaction.account_id,
        "type": transaction.tx_type,
        "amount": transaction.amount,
        "timestamp": transaction.timestamp,
    }

