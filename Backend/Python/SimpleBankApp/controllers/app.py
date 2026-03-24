from pathlib import Path
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

# Allow running this file directly while importing sibling MVC packages.
APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from services.account_service import AccountService
from views.bank_view import account_to_dict, transaction_to_dict, user_to_dict


app = Flask(__name__)
CORS(app)

user_repository = UserRepository()
account_repository = AccountRepository()
transaction_repository = TransactionRepository()
account_service = AccountService(account_repository, transaction_repository)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    existing = user_repository.get_by_username(username)
    if existing is not None:
        return jsonify({"error": "Username already exists"}), 400

    user = user_repository.add(username=username, password=password)
    return jsonify({"message": "User registered successfully", "user": user_to_dict(user)}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    user = user_repository.get_by_username(username or "")
    if user is None or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "username": user.username}), 200


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json(silent=True) or {}
    user_id = data.get("userId")
    account_type = data.get("accountType")

    if user_id is None or not account_type:
        return jsonify({"error": "userId and accountType are required"}), 400

    try:
        account = account_service.createAccount(userId=int(user_id), accountType=str(account_type))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(account_to_dict(account)), 201


@app.route("/api/accounts/<account_id>", methods=["GET"])
def get_account(account_id: str):
    account = account_service.getAccount(accountId=account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account_to_dict(account)), 200


@app.route("/api/accounts/<account_id>/deposit", methods=["POST"])
def deposit(account_id: str):
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
    try:
        tx_list = account_service.getTransactions(accountId=account_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify([transaction_to_dict(tx) for tx in tx_list]), 200


if __name__ == "__main__":
    app.run(debug=True)
