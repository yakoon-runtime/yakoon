from typing import Optional
from yakoon.platform.models.account import Account


class InMemoryAccountStore:

    def __init__(self):
        self._accounts: dict[str, Account] = {}
        load_defaults(self)

    def get_by_name(self, name: str) -> Optional[Account]:
        for account in self._accounts.values():
            if account.name.lower() == name.lower():
                return account
        return None

    def get_by_id(self, account_id: str) -> Optional[Account]:
        return self._accounts.get(account_id)

    def all(self) -> list[Account]:
        return list(self._accounts.values())

    def exists(self, name: str) -> bool:
        return self.get_by_name(name) is not None

    def add(self, account: Account):
        self._accounts[account.id] = account


def load_defaults(store: InMemoryAccountStore):

    default_groups = {
        "group 1": ["realm:system", "realm:account", "realm:character"]
    }

    store.add(Account(id="acc-stefan", name="Stefan", cmd_groups=default_groups["group 1"]))
    store.add(Account(id="acc-lara", name="Lara", cmd_groups=["system"]))
