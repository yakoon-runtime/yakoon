from typing import Dict, Optional
from yakoon.domains.game.models.character import Character


class CharacterStore:
    _chars: dict[str, Character] = {}

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Character]:
        for key, character in cls._chars.items():
            if character.name.lower() == name.lower():
                return cls._chars[key]

    @classmethod
    def get_by_id(cls, char_id: str) -> Optional[Character]:
        return cls._chars.get(char_id)

    @classmethod
    def add(cls, obj: Character):
        cls._chars[obj.id] = obj

    @classmethod
    def all(cls) -> list[Character]:
        return list(cls._chars.values())

    @classmethod
    def exists(cls, char_id: str) -> bool:
        return char_id in cls._chars

CharacterStore.add(
    Character(id="char-stefan", name="Stefan", location="forest"))
CharacterStore.add(
    Character(id="char-lara", name="Lara", location="hall"))