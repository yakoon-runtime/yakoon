from typing import Optional
from yakoon.domains.gateway.models.account import Account


class InMemoryAccountStore:

    def __init__(self):
        self._accounts: dict[str, Account] = {}
        load_defaults(self)

    async def get_by_name(self, name: str) -> Optional[Account]:
        for account in self._accounts.values():
            if account.name.lower() == name.lower():
                return account
        return None

    async def get_by_id(self, account_id: str) -> Optional[Account]:
        return self._accounts.get(account_id)

    async def delete_by_id(self, account_id: str) -> None:
        self._accounts.pop(account_id, None)
     
    async def save(self, account: Account) -> None:
        pass

    def add(self, account: Account):
        self._accounts[account.id] = account


def load_defaults(store: InMemoryAccountStore):

    default_groups = {
        "group 1": ["realm:system", "realm:account", "realm:character"]
    }

    store.add(Account(id="acc-stefan", name="Stefan", cmd_groups=default_groups["group 1"]))
    store.add(Account(id="acc-lara", name="Lara", cmd_groups=["system"]))
