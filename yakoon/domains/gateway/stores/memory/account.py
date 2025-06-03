from typing import Optional
from yakoon.domains.gateway.models.account import Account
from yakoon.stores.memory.base_store import MemoryStore


class InMemoryAccountStore(MemoryStore):

    def __init__(self):
        super().__init__()
        load_defaults(self)

    async def get_by_id(self, account_id: str) -> Optional[Account]:
        row = await super().get_by_id(account_id)
        return Account.from_row(row) if row else None

    async def get_by_name(self, name: str) -> Optional[Account]:
        all_accounts = await self.fetch_by_fields()
        for row in all_accounts:
            acc = Account.from_row(row)
            if acc.name.lower() == name.lower():
                return acc
        return None

    async def delete_by_id(self, account_id: str) -> None:
        await super().delete(account_id)

    async def save(self, account: Account) -> None:
        await super().save(account.to_row())

    def add(self, account: Account):
        self._data[account.id] = account.to_row()



def load_defaults(store: InMemoryAccountStore):

    default_groups = {
        "group 1": ["realm:system", "realm:account", "realm:character"]
    }

    store.add(Account(id="acc-stefan", name="Stefan", cmd_groups=default_groups["group 1"]))
    store.add(Account(id="acc-lara", name="Lara", cmd_groups=["system"]))
