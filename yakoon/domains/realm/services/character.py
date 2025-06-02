from argparse import Namespace
from typing import Optional
from yakoon.domains.realm.models.character import Character


class CharacterService:
    
    def __init__(self, store):
        self.store = store

    async def get_by_id(self, ns: Namespace, char_id: str) -> Optional[Character]:
        return await self.store.get_by_id(ns, char_id)

    async def get_by_name(self, ns: Namespace, name: str) -> Optional[Character]:
        return await self.store.get_by_name(ns, name)
    
    async def save(self, char: Character):
        await self.store.save(char)
