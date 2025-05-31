
from __future__ import annotations
from yakoon.runtime.models.data import RuntimeSessionData

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from yakoon.domains.realm.models.character import Character


class RuntimeRealmData(RuntimeSessionData):

    def __init__(self, character: Character=None):
        super().__init__()
        self._character = character

    @property
    def character(self) -> Character | None:
        return self._character

    @character.setter
    def character(self, value):
        self._character = value

    def is_ic(self) -> bool:
        return self.character is not None