
from typing import Optional
from yakoon.saas.controllers.gateway.models.account import Account
from yakoon.saas.models.key import Key
from yakoon.saas.models.namespace import Namespace

class AccountService:

    def __init__(self, store):
        self.store = store

    async def get_by_key(self, key: Key) -> Optional[Account]:
        row = await self.store.get_by_key(key)
        return Account.from_row(row) if row else None

    async def get_by_name(self, namespace: Namespace, name: str) -> Optional[Account]:
        rows = await self.store.fetch_by_fields(namespace=namespace, name=name, limit=1)        
        return Account.from_row(rows[0]) if rows else None
    
    async def save(self, account: Account):
        account.validate()
        await self.store.save(account.to_row())

    async def delete_by_key(self, key: Key):
        await self.store.delete_by_key(key)
 