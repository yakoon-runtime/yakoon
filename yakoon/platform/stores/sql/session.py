from dataclasses import asdict

from sqlalchemy import Column, String, Boolean
from sqlalchemy.future import select
from yakoon.platform.runtime.session import PlatformSession
from yakoon.platform.stores.sql._base import Base


class SessionORM(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False)
    character_id = Column(String, nullable=False)
    connection_type = Column(String, nullable=False)
    connected = Column(Boolean, default=True)

# ─────────────────────────────────────────────────────────────

class SQLSessionStore:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, id_: str) -> PlatformSession | None:
        stmt = select(SessionORM).where(SessionORM.id == id_)
        result = self.db.execute(stmt).scalar_one_or_none()
        return self._to_entity(result) if result else None

    def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        existing = self.get_by_id(session_id)
        if existing:
            return existing, False
        new = PlatformSession(id=session_id, **kwargs)
        self.save(new)
        return new, True

    def save(self, session: PlatformSession):
        orm = self._to_orm(session)
        self.db.merge(orm)  # insert or update
        self.db.commit()

    # ─────────── Mapping ───────────

    def _to_orm(self, session: PlatformSession) -> SessionORM:
        return SessionORM(**asdict(session))

    def _to_entity(self, orm: SessionORM) -> PlatformSession:
        return PlatformSession(
            id=orm.id,
            account_id=orm.account_id,
            character_id=orm.character_id,
            connection_type=orm.connection_type,
            connected=orm.connected
        )
