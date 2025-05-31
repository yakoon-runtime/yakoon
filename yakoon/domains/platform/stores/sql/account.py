from dataclasses import asdict

from sqlalchemy import JSON, Column, String
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from yakoon.domains.platform.models.account import Account
from yakoon.domains.platform.stores.sql._base import Base


class AccountORM(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True)
    name = Column(String(30), nullable=False)
    cmd_groups = Column(JSON, default=[]) 

# ─────────────────────────────────────────────────────────────

class SQLAccountStore:

    def __init__(self, db_session: Session):
        self.db = db_session

    async def get_by_id(self, id_: str) -> Account | None:
        stmt = select(AccountORM).where(AccountORM.id == id_)
        result = self.db.execute(stmt).scalar_one_or_none()
        return _to_entity(result) if result else None

    async def get_by_name(self, name: str) -> Account | None:
        stmt = select(AccountORM).where(AccountORM.name == name)
        result = self.db.execute(stmt).scalar_one_or_none()
        return _to_entity(result) if result else None

    async def save(self, account: Account):
        orm = _to_orm(account)
        self.db.merge(orm)  # insert or update
        self.db.commit()

    async def delete_by_id(self, id_: str):
        orm = self.db.get(AccountORM, id_)
        if orm:
            self.db.delete(orm)
            self.db.commit()

  # ─────────── Mapping ───────────

def _to_orm(account: Account) -> dict:
    return AccountORM(
        id=account.id,
        name=account.name,
        cmd_groups=account.cmd_groups,
    )

def _to_entity(row: AccountORM) -> Account:
    return Account(
        id=row.id,
        name=row.name,
        cmd_groups=row.cmd_groups or [],
    )

