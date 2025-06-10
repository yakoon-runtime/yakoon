from argparse import Namespace
from typing import Optional
from yakoon.saas.domains.realm.models.character import Character
from typing import Optional

from yakoon.mesh.models.key import Key


class CharacterService:
    
    def __init__(self, store):
        self.store = store

    async def get_by_key(self, key: Key) -> Optional[Character]:
        row = await self.store.get_by_key(key)
        return Character.from_row(row) if row else None

    async def get_by_name(self, namespace: Namespace, name: str) -> Optional[Character]:
        rows = await self.store.fetch_by_fields(namespace=namespace, name=name, limit=1)        
        return Character.from_row(rows[0]) if rows else None
    
    async def save(self, character: Character):
        character.validate()
        await self.store.save(character.to_row())

    async def delete_by_key(self, key: Key):
        await self.store.delete_by_key(key)
