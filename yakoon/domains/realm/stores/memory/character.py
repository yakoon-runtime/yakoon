
from typing import Optional
from yakoon.domains.realm.models.character import Character


class InMemoryCharacterStore:
    
    def __init__(self):
        self._chars: dict[str, Character] = {}
        load_defaults(self)

    def get_by_name(self, name: str) -> Optional[Character]:
        for char in self._chars.values():
            if char.name.lower() == name.lower():
                return char

    def get_by_id(self, char_id: str) -> Optional[Character]:
        return self._chars.get(char_id)

    def add(self, obj: Character):
        self._chars[obj.id] = obj

    def all(self) -> list[Character]:
        return list(self._chars.values())

    def exists(self, char_id: str) -> bool:
        return char_id in self._chars

    def save(self, obj: Character):
        pass  # optional später


def load_defaults(store: InMemoryCharacterStore):
    store.add(
        Character(id="char-stefan", name="Stefan", location="forest"))
    store.add(
        Character(id="char-lara", name="Lara", location="hall"))