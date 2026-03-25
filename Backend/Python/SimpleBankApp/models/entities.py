from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    user_id: int
    username: str
    email: str


@dataclass
class Account:
    account_id: str
    user_id: int
    account_type: str
    balance: float = 0.0


@dataclass
class Transaction:
    account_id: str
    tx_type: str
    amount: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

