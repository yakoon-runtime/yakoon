from yakoon.runtime.models.data import RuntimeSessionData
from yakoon.platform.services.account import AccountService
from yakoon.platform.runtime.session import PlatformSession
from yakoon.services.base.session import BaseSessionService


class SessionService(BaseSessionService):
    
    @classmethod
    async def get_by_id(cls, session_id: str) -> PlatformSession:
        return await cls.store.get_by_id(session_id)

    @classmethod
    async def get_or_create(cls, session_id: str, **kwargs) -> tuple[PlatformSession, bool]:
        session, created = await cls.store.get_or_create(session_id, **kwargs)
        if not created:
            await cls.restore_account(session, **kwargs)
        session.data_runtime = RuntimeSessionData() # to avoid runtime state leaks
        return session, created

    @classmethod
    async def save(cls, session: PlatformSession):
        await cls.store.save(session)

    @classmethod
    async def delete_by_id(cls, session_id: str):
        await cls.store.delete_by_id(session_id)

    @classmethod
    async def restore_account(cls, session: PlatformSession, **kwargs):
        account_id = kwargs.get("account_id", session.account_id)
        account_id_was_none = not session.account_id 
        if account_id and not session.account:
            account = await AccountService.get_by_id(account_id)
            session.account_id = account_id
            session.account = account
        if account_id_was_none:
            await cls.store.save(session)
        
