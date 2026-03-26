from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, TIMESTAMP, text

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class AccountModel(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    balance = Column(DECIMAL(10, 2), default=0)
    account_type = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class TransactionModel(Base):
    __tablename__ = "transactions"

    txn_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    txn_type = Column(String(20))
    amount = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
