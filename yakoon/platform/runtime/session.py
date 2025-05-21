
from __future__ import annotations
from yakoon.engine.system.session import BaseSession
from yakoon.platform.models.account import Account


class PlatformSession(BaseSession):

    def __init__(self, id: str):
        super().__init__(id)
        self._permissions = ["system"]
        self._account = None

    @property
    def account(self) -> Account | None:
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    def is_anonymous(self) -> bool:
        return self.account is None

    @property
    def permissions(self) -> list[str]:
        return self._permissions or []

    @permissions.setter
    def permissions(self, value: list[str]):
        self._permissions = value
