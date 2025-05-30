from yakoon.platform.services.account import AccountService
from yakoon.platform.stores.session import BaseSessionStore
from yakoon.engine.services.session import BaseSessionService
from yakoon.platform.runtime.session import PlatformSession


class SessionService(BaseSessionService):
    
    store: BaseSessionStore = None

    @classmethod
    def bind_storage(cls, store):
        cls.store = store

    @classmethod
    async def get_by_id(cls, session_id: str) -> PlatformSession:
        return await cls.store.get_by_id(session_id)

    @classmethod
    async def get_or_create(cls, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        session, created = await cls.store.get_or_create(session_id, **kwargs)
        if session:
            await cls.restore_account(session, **kwargs)
        return session, created

    @classmethod
    async def persist(cls, session: PlatformSession):
        await cls.store.persist(session)

    @classmethod
    async def delete(cls, session_id: str):
        await cls.store.delete(session_id)

    @classmethod
    async def restore_account(cls, session: PlatformSession, **kwargs):
        account_id = kwargs.get("account_id", session.account_id)
        if account_id and session.is_anonymous:
            account = AccountService.get_by_id(account_id)
            session.account_id = account_id
            session.account = account
        #if session.account:
            #session.cmd_groups = account.groups