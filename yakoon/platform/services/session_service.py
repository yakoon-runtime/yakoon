# yakoon/platform/session_service.py
from yakoon.platform.stores.account_store import AccountStore
from yakoon.platform.stores.session_store import SessionStore
from yakoon.engine.services.session_service import BaseSessionService
from yakoon.platform.runtime.session import PlatformSession


class SessionService(BaseSessionService):
    
    def __init__(self, store: SessionStore):
        self.store = store

    async def get_by_id(self, session_id: str) -> PlatformSession:
        return await self.store.get_by_id(session_id)

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        session, created = await self.store.get_or_create(session_id)
        if getattr(session, "account_id", None):
            await self.restore_account(session, **kwargs)
        else:
            session.command_groups = ["login"]
        return session, created

    async def persist(self, session: PlatformSession):
        await self.store.persist(session)

    async def delete(self, session_id: str):
        await self.store.delete(session_id)

    async def restore_account(session: PlatformSession, **kwargs):
        if session.is_anonymous:
            account = AccountStore.get_by_id(kwargs["account_id"])
            session.account = account
        if session.account:
            session.command_groups = account.groups