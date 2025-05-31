from yakoon.runtime.models.data import RuntimeSessionData
from yakoon.domains.platform.services.account import AccountService
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.services.base.session import BaseSessionService


class SessionService(BaseSessionService):
    
    def __init__(self, store):
        self.store = store

    async def get_by_id(self, session_id: str) -> PlatformSession:
        return await self.store.get_by_id(session_id)

    async def get_or_create(self, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        session, created = await self.store.get_or_create(session_id, **kwargs)
        if not created:
            await self.restore_account(session, **kwargs)
        session.data_runtime = RuntimeSessionData() # to avoid runtime state leaks
        return session, created

    async def save(self, session: PlatformSession):
        await self.store.save(session)

    async def delete_by_id(self, session_id: str):
        await self.store.delete_by_id(session_id)

    async def restore_account(self, session: PlatformSession, **kwargs):
        services = session.ctx.platform.services.get_registry("system")
        account_id = kwargs.get("account_id", session.account_id)
        account_id_was_none = not session.account_id 
        if account_id and not session.account:
            account = await services.accounts.get_by_id(account_id)
            session.account_id = account_id
            session.account = account
        if account_id_was_none:
            await self.store.save(session)
    