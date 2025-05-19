
from __future__ import annotations
from engine.runtime.session import BaseSession

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mygame.models.account import Account
    from mygame.models.character import Character


class GameSession(BaseSession):

    def __init__(self, id: str):
        super().__init__(id)
        self._account = None
        self._character = None

    @property
    def account(self) -> Account | None:
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def character(self) -> Character | None:
        return self._character

    @character.setter
    def character(self, value):
        self._character = value

    def is_anonymous(self) -> bool:
        return self.account is None

    def is_ic(self) -> bool:
        return self.character is not None

    def is_ooc(self) -> bool:
        return self.account is not None and self.character is None
