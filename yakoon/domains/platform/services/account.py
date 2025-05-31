
from typing import Optional
from yakoon.domains.platform.models.account import Account

class AccountService:

    store = None

    @classmethod
    def bind_storage(cls, store):
        cls.store = store

    @classmethod
    async def get_by_id(cls, id_: str) -> Optional[Account]:
        return await cls.store.get_by_id(id_)

    @classmethod
    async def get_by_name(cls, name: str) -> Optional[Account]:
        return await cls.store.get_by_name(name)

    @classmethod
    async def all(cls) -> list[Account]:
        return await cls.store.all()

    @classmethod
    async def exists(cls, name: str) -> bool:
        return await cls.store.exists(name)

    @classmethod
    async def save(cls, account: Account):
        account.validate()
        await cls.store.save(account)