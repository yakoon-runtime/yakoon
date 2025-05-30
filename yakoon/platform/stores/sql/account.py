from dataclasses import asdict

from sqlalchemy import JSON, Column, String
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from yakoon.platform.models.account import Account
from yakoon.platform.stores.sql._base import Base


class AccountORM(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True)
    name = Column(String(30), nullable=False)
    cmd_groups = Column(JSON, default=[])  # SQLite unterstützt JSON nativ

# ─────────────────────────────────────────────────────────────

class SQLAccountStore:

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, id_: str) -> Account | None:
        stmt = select(AccountORM).where(AccountORM.id == id_)
        result = self.db.execute(stmt).scalar_one_or_none()
        return from_row(result.__dict__) if result else None

    def get_by_name(self, name: str) -> Account | None:
        stmt = select(AccountORM).where(AccountORM.name == name)
        result = self.db.execute(stmt).scalar_one_or_none()
        return from_row(result.__dict__) if result else None

    def save(self, account: Account):
        row = to_row(account)
        orm = AccountORM(**row)
        self.db.merge(orm)
        self.db.commit()

  # ─────────── Mapping ───────────

def to_row(account: Account) -> dict:
    return asdict(account)

def from_row(row: dict) -> Account:
    return Account(**row)