
from typing import Optional
from yakoon.platform.models.account import Account
from yakoon.platform.stores.memory.account import InMemoryAccountStore


class AccountService:

    store = InMemoryAccountStore()

    @classmethod
    def get_by_id(cls, id_: str) -> Optional[Account]:
        return cls.store.get_by_id(id_)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Account]:
        return cls.store.get_by_name(name)

    @classmethod
    def all(cls) -> list[Account]:
        return cls.store.all()

    @classmethod
    def exists(cls, name: str) -> bool:
        return cls.store.exists(name)
