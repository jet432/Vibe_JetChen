import os
from pathlib import Path
from threading import Lock

from pymongo import ASCENDING, MongoClient, ReturnDocument

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv is not None:
    # Load .env from the project root for local development defaults.
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")


_mongo_client: MongoClient | None = None
_mongo_db = None
_mongo_lock = Lock()


def _build_mongo_client() -> tuple[MongoClient, str]:
    uri = os.getenv("MONGODB_URI", "").strip()
    db_name = os.getenv("MONGODB_DB_NAME", "").strip()
    if not uri or not db_name:
        raise RuntimeError("MONGODB_URI and MONGODB_DB_NAME environment variables are required")
    client = MongoClient(uri)
    return client, db_name


def get_db():
    global _mongo_client, _mongo_db
    if _mongo_db is not None:
        return _mongo_db

    with _mongo_lock:
        if _mongo_db is None:
            client, db_name = _build_mongo_client()
            _mongo_client = client
            _mongo_db = client[db_name]
    return _mongo_db


def init_db() -> None:
    db = get_db()
    db.command("ping")

    db.users.create_index([("user_id", ASCENDING)], unique=True)
    db.users.create_index([("name", ASCENDING)], unique=True)
    db.users.create_index([("email", ASCENDING)], unique=True)

    db.accounts.create_index([("account_id", ASCENDING)], unique=True)
    db.accounts.create_index([("user_id", ASCENDING)])

    db.transactions.create_index([("txn_id", ASCENDING)], unique=True)
    db.transactions.create_index([("account_id", ASCENDING), ("txn_id", ASCENDING)])


def get_next_sequence(name: str) -> int:
    db = get_db()
    row = db.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(row["value"])