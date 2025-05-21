from typing import Dict, Optional
from yakoon.domains.game.models.character import Character


class CharacterStore:
    _chars: dict[str, Character] = {}

    @classmethod
    def get(cls, char_id: str) -> Optional[Character]:
        return cls._chars.get(char_id)

    @classmethod
    def put(cls, obj: Character):
        cls._chars[obj.id] = obj

    @classmethod
    def all(cls) -> list[Character]:
        return list(cls._chars.values())

    @classmethod
    def exists(cls, char_id: str) -> bool:
        return char_id in cls._chars

CharacterStore.put(
    Character(id="stefan", name="Stefan", location="forest"))
CharacterStore.put(
    Character(id="lara", name="Lara", location="hall"))