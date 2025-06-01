from typing import Optional
from yakoon.domains.realm.models.character import Character


class CharacterService:
    
    def __init__(self, store):
        self.store = store

    async def get_by_id(self, char_id: str) -> Optional[Character]:
        return await self.store.get_by_id(char_id)

    async def get_by_name(self, name: str) -> Optional[Character]:
        return await self.store.get_by_name(name)

    async def all(self) -> list[Character]:
        return await self.store.all()

    async def exists(self, char_id: str) -> bool:
        return await self.store.exists(char_id)
    
    async def save(self, char: Character):
        await self.store.save(char)
