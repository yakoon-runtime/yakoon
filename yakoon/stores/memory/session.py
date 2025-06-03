from typing import Optional

from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.stores.memory.base_store import MemoryStore


class InMemorySessionStore(MemoryStore):

    def __init__(self):
        super().__init__()

    async def get_by_id(self, session_id: str) -> Optional[GatewaySession]:
        row = await super().get_by_id(session_id)
        return GatewaySession.from_row(row) if row else None

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[GatewaySession, bool]:
        existing = await self.get_by_id(session_id)
        if existing:
            return existing, False

        new_session = GatewaySession(id=session_id, **kwargs)
        await self.save(new_session)
        return new_session, True

    async def save(self, session: GatewaySession) -> None:
        await super().save(session.to_row())

    async def delete_by_id(self, session_id: str) -> None:
        await super().delete(session_id)
