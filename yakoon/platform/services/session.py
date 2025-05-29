from yakoon.platform.services.account import AccountService
from yakoon.platform.stores.session import BaseSessionStore
from yakoon.engine.services.session import BaseSessionService
from yakoon.platform.runtime.session import PlatformSession


class SessionService(BaseSessionService):
    
    def __init__(self, store: BaseSessionStore):
        self.store = store

    async def get_by_id(self, session_id: str) -> PlatformSession:
        return await self.store.get_by_id(session_id)

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        session, created = await self.store.get_or_create(session_id, **kwargs)
        if session:
            await self.restore_account(session, **kwargs)
        return session, created

    async def persist(self, session: PlatformSession):
        await self.store.persist(session)

    async def delete(self, session_id: str):
        await self.store.delete(session_id)

    async def restore_account(self, session: PlatformSession, **kwargs):
        account_id = kwargs.get("account_id", session.account_id)
        if account_id and session.is_anonymous:
            account = AccountService.get_by_id(account_id)
            session.account_id = account_id
            session.account = account
        #if session.account:
            #session.cmd_groups = account.groups