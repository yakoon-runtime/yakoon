
from typing import Optional
from yakoon.domains.platform.models.account import Account

class AccountService:

    store = None

    def __init__(self, store):
        self.store = store

    async def get_by_id(self, id_: str) -> Optional[Account]:
        return await self.store.get_by_id(id_)

    async def get_by_name(self, name: str) -> Optional[Account]:
        return await self.store.get_by_name(name)

    async def all(self) -> list[Account]:
        return await self.store.all()

    async def exists(self, name: str) -> bool:
        return await self.store.exists(name)

    async def save(self, account: Account):
        account.validate()
        await self.store.save(account)