from pathlib import Path
from datetime import datetime, timedelta, timezone
import os
import sys

import bcrypt
import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

# Allow running this file directly while importing sibling MVC packages.
APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from repositories.account_repository import AccountRepository
from database import init_db
from models.entities import Account, Transaction, User
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from services.account_service import AccountService


app = Flask(__name__)
CORS(app)
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", "12"))
try:
    init_db()
except Exception as exc:
    raise RuntimeError(
        "Database initialization failed. Set MONGODB_URI and MONGODB_DB_NAME "
        "environment variables before starting the API."
    ) from exc

user_repository = UserRepository()
account_repository = AccountRepository()
transaction_repository = TransactionRepository()
account_service = AccountService(account_repository, transaction_repository)


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
        "transactionId": transaction.txn_id,
        "type": transaction.tx_type,
        "amount": transaction.amount,
        "date": date_value,
    }


def hash_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(raw_password: str, stored_password: str) -> bool:
    if stored_password.startswith("$2a$") or stored_password.startswith("$2b$") or stored_password.startswith("$2y$"):
        return bcrypt.checkpw(raw_password.encode("utf-8"), stored_password.encode("utf-8"))
    return raw_password == stored_password


def create_access_token(user_id: int, email: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXP_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user_id() -> tuple[int | None, tuple[dict, int] | None]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, ({"error": "Missing or invalid Authorization header"}, 401)

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id, None
    except jwt.ExpiredSignatureError:
        return None, ({"error": "Token expired"}, 401)
    except (jwt.InvalidTokenError, TypeError, ValueError):
        return None, ({"error": "Invalid token"}, 401)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("name") or data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    existing = user_repository.get_by_username(username)
    if existing is not None:
        return jsonify({"error": "User name already exists"}), 400

    existing_email = user_repository.get_by_email(email)
    if existing_email is not None:
        return jsonify({"error": "Email already exists"}), 400

    password_hash = hash_password(str(password))
    user = user_repository.add(username=username, email=email, password=password_hash)
    return jsonify({"message": "User registered successfully", "user": user_to_dict(user)}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = user_repository.get_by_email(str(email))
    if user is None or not verify_password(str(password), user.password or ""):
        return jsonify({"error": "Invalid email or password"}), 401

    # If legacy plaintext password exists, transparently migrate it to bcrypt.
    if not (user.password or "").startswith("$2"):
        user_repository.update_password(user.user_id, hash_password(str(password)))

    access_token = create_access_token(user.user_id, user.email)
    accounts = account_repository.get_for_user(user.user_id)
    return (
        jsonify(
            {
                "message": "Login successful",
                "token": access_token,
                "user": user_to_dict(user),
                "accounts": [account_to_dict(account) for account in accounts],
            }
        ),
        200,
    )


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json(silent=True) or {}
    user_id = data.get("userId")
    account_type = data.get("accountType")

    if user_id is None or not account_type:
        return jsonify({"error": "userId and accountType are required"}), 400

    user = user_repository.get_by_id(int(user_id))
    if user is None:
        return jsonify({"error": "User not found"}), 404

    try:
        account = account_service.createAccount(userId=int(user_id), accountType=str(account_type))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(account_to_dict(account)), 201


@app.route("/api/accounts/<account_id>", methods=["GET"])
def get_account(account_id: str):
    current_user_id, auth_error = get_current_user_id()
    if auth_error:
        body, status = auth_error
        return jsonify(body), status

    account = account_service.getAccount(accountId=account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    if account.user_id != current_user_id:
        return jsonify({"error": "Forbidden"}), 403
    user = user_repository.get_by_id(account.user_id)
    user_name = user.username if user else None
    return jsonify(account_response(account, user_name)), 200


@app.route("/api/accounts/<account_id>/deposit", methods=["POST"])
def deposit(account_id: str):
    current_user_id, auth_error = get_current_user_id()
    if auth_error:
        body, status = auth_error
        return jsonify(body), status

    account = account_service.getAccount(accountId=account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    if account.user_id != current_user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    amount = data.get("amount")
    if amount is None:
        return jsonify({"error": "amount is required"}), 400

    try:
        account = account_service.deposit(accountId=account_id, amount=float(amount))
    except ValueError as exc:
        status = 404 if str(exc) == "Account not found" else 400
        return jsonify({"error": str(exc)}), status

    return jsonify(account_to_dict(account)), 200


@app.route("/api/accounts/<account_id>/withdraw", methods=["POST"])
def withdraw(account_id: str):
    current_user_id, auth_error = get_current_user_id()
    if auth_error:
        body, status = auth_error
        return jsonify(body), status

    account = account_service.getAccount(accountId=account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    if account.user_id != current_user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    amount = data.get("amount")
    if amount is None:
        return jsonify({"error": "amount is required"}), 400

    try:
        account = account_service.withdraw(accountId=account_id, amount=float(amount))
    except ValueError as exc:
        status = 404 if str(exc) == "Account not found" else 400
        return jsonify({"error": str(exc)}), status

    return jsonify(account_to_dict(account)), 200


@app.route("/api/accounts/<account_id>/transactions", methods=["GET"])
def get_transactions(account_id: str):
    current_user_id, auth_error = get_current_user_id()
    if auth_error:
        body, status = auth_error
        return jsonify(body), status

    account = account_service.getAccount(accountId=account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    if account.user_id != current_user_id:
        return jsonify({"error": "Forbidden"}), 403

    try:
        tx_list = account_service.getTransactions(accountId=account_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify([transaction_to_dict(tx) for tx in tx_list]), 200


if __name__ == "__main__":
    app.run(debug=True)
