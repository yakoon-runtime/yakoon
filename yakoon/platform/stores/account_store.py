from typing import Optional
from yakoon.platform.models.account import Account


class AccountStore:
    _accounts: dict[str, Account] = {}

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Account]:
        for key, account in cls._accounts.items():
            if account.name == name.lower():
                return cls._accounts[key]

    @classmethod
    def get_by_id(cls, account_id: str) -> Optional[Account]:
        return cls._accounts.get(account_id)

    @classmethod
    def all(cls) -> list[Account]:
        return list(cls._accounts.values())

    @classmethod
    def exists(cls, name: str) -> bool:
        return cls.get_by_name(name) != None

    @classmethod
    def add(cls, account: Account):
        cls._accounts[account.id] = account

default_groups = {
   "group 1": ["mud:system","mud:account"]
}


AccountStore.add(Account(id="acc-stefan", name="stefan", cmd_groups=default_groups["group 1"]))
AccountStore.add(Account(id="acc-lara", name="lara", cmd_groups=["system"]))