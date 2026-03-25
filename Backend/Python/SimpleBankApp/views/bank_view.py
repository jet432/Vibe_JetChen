from models.entities import Account, Transaction, User


def user_to_dict(user: User) -> dict:
    return {"userId": user.user_id, "name": user.username, "email": user.email}


def account_to_dict(account: Account) -> dict:
    return {
        "accountId": int(account.account_id),
        "userId": account.user_id,
        "accountType": account.account_type,
        "balance": account.balance,
    }


def account_response(account: Account, user_name: str | None) -> dict:
    return {
        "accountId": int(account.account_id),
        "userName": user_name,
        "balance": account.balance,
    }


def transaction_to_dict(transaction: Transaction) -> dict:
    date_value = (transaction.timestamp or "")[:10]
    return {
        "type": transaction.tx_type,
        "amount": transaction.amount,
        "date": date_value,
    }
