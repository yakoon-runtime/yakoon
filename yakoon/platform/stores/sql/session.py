from dataclasses import asdict

from sqlalchemy import JSON, Column, DateTime, String, Boolean
from sqlalchemy.future import select
from yakoon.engine.system.data import StorageSessionData
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.stores.sql._base import Base


class SessionORM(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    lang = Column(String)
    cmd_groups = Column(JSON)
    data_storage = Column(JSON)
    
    account_id = Column(String)
    permissions = Column(JSON)
    timestamp = Column(DateTime)

# ─────────────────────────────────────────────────────────────

class SQLSessionStore:
    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id_: str) -> PlatformSession | None:
        stmt = select(SessionORM).where(SessionORM.id == id_)
        result = self.db.execute(stmt).scalar_one_or_none()
        return self._to_entity(result) if result else None

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        existing = await self.get_by_id(session_id)
        if existing:
            return existing, False
        new = PlatformSession(id=session_id, **kwargs)
        await self.save(new)
        return new, True

    async def save(self, session: PlatformSession):
        orm = self._to_orm(session)
        self.db.merge(orm)  # insert or update
        self.db.commit()

    async def delete_by_id(self, session_id: str):
        orm = self.db.get(SessionORM, session_id)
        if orm:
            self.db.delete(orm)
            self.db.commit()

    # ─────────── Mapping ───────────

    def _to_orm(self, session: PlatformSession) -> SessionORM:
          return SessionORM(
            id=session.id,
            lang=session.lang,
            cmd_groups=session.cmd_groups,
            data_storage=session.data_storage.to_dict(),
            account_id=session.account_id,
            permissions=session.permissions,
            timestamp=session.timestamp,
        )
    
    def _to_entity(self, orm: SessionORM) -> PlatformSession:
        return PlatformSession(
            id=orm.id,
            lang=orm.lang,
            cmd_groups=orm.cmd_groups or [],
            data_storage=StorageSessionData.from_dict(orm.data_storage or {}),
            account_id=orm.account_id,
            permissions=orm.permissions,
            timestamp=orm.timestamp,
            )