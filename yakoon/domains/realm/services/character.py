
from typing import Optional
from yakoon.domains.realm.models import Character
from yakoon.domains.realm.stores.memory.character import InMemoryCharacterStore


class CharacterService:
    
    store = InMemoryCharacterStore()

    @classmethod
    def get_by_id(cls, char_id: str) -> Optional[Character]:
        return cls.store.get_by_id(char_id)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Character]:
        return cls.store.get_by_name(name)

    @classmethod
    def all(cls) -> list[Character]:
        return cls.store.all()

    @classmethod
    def exists(cls, char_id: str) -> bool:
        return cls.store.exists(char_id)
    
    @classmethod
    def persist(cls, char: Character):
        cls.store.persist(char)
