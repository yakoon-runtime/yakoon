from dataclasses import asdict

from sqlalchemy import JSON, Column, DateTime, String, Boolean
from sqlalchemy.future import select
from yakoon.runtime.models.data import StorageSessionData
from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.domains.gateway.stores.___sql._base import Base


class SessionORM(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    domain_id = Column(String)
    lang = Column(String)
    data_storage = Column(JSON)
    
    account_id = Column(String)
    permissions = Column(JSON)
    timestamp = Column(DateTime)

# ─────────────────────────────────────────────────────────────

class SQLSessionStore:
    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id_: str) -> GatewaySession | None:
        stmt = select(SessionORM).where(SessionORM.id == id_)
        result = self.db.execute(stmt).scalar_one_or_none()
        return self._to_entity(result) if result else None

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[GatewaySession, bool]:
        existing = await self.get_by_id(session_id)
        if existing:
            return existing, False
        new = GatewaySession(id=session_id, **kwargs)
        await self.save(new)
        return new, True

    async def save(self, session: GatewaySession):
        orm = self._to_orm(session)
        self.db.merge(orm)  # insert or update
        self.db.commit()

    async def delete_by_id(self, session_id: str):
        orm = self.db.get(SessionORM, session_id)
        if orm:
            self.db.delete(orm)
            self.db.commit()

    # ─────────── Mapping ───────────

    def _to_orm(self, session: GatewaySession) -> SessionORM:
          return SessionORM(
            id=session.id,
            lang=session.lang,
            domain_id=session.domain_id,
            data_storage=session.data_storage.to_dict(),
            account_id=session.account_id,
            permissions=session.permissions,
            timestamp=session.timestamp,
        )
    
    def _to_entity(self, orm: SessionORM) -> GatewaySession:
        return GatewaySession(
            id=orm.id,
            lang=orm.lang,
            domain_id=orm.domain_id,
            data_storage=StorageSessionData.from_dict(orm.data_storage or {}),
            account_id=orm.account_id,
            permissions=orm.permissions,
            timestamp=orm.timestamp,
            )