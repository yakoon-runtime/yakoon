from typing import Optional
from mygame.models.account import Account


class AccountStore:
    _accounts: dict[str, Account] = {}

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Account]:
        return cls._accounts.get(name.lower())

    @classmethod
    def all(clf) -> list[Account]:
        return list(cls._accounts.values())

    @classmethod
    def exists(cls, name: str) -> bool:
        return name.lower() in cls._accounts

    @classmethod
    def add(cls, account: Account):
        cls._accounts[account.name.lower()] = account


AccountStore.add(Account(id="acc-stefan", name="stefan"))
AccountStore.add(Account(id="acc-lara", name="lara"))