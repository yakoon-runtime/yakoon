from abc import ABC
from yakoon.models.key import Key
from typing import Any, Optional
import copy

from yakoon.stores.base.base_store import BaseStore


class MemoryStore(BaseStore, ABC):
    """
    In-memory implementation of the Store interface.
    Used for testing and ephemeral session data.
    """

    def __init__(self):
        self._data: dict[str, dict] = {}

    async def get_by_id(self, id: str) -> Optional[dict]:
        obj = self._data.get(id)
        return copy.deepcopy(obj) if obj else None

    async def get_by_key(self, key: Key) -> Optional[dict]:
        return await self.get_by_id(key.to_str())

    async def fetch_by_namespace(self, namespace: str, *, limit: int = 100) -> list[dict]:
        return [copy.deepcopy(obj) for obj in self._data.values() if obj.get("namespace") == namespace][0:limit]

    async def fetch_by_fields(self, *, limit: int = 100, **fields: Any) -> list[dict]:
        return [
            obj for obj in self._data.values()
            if all(obj.get(k) == v for k, v in fields.items())
        ][0:limit]

    async def save(self, obj: dict) -> None:
        self._data[obj["id"]] = copy.deepcopy(obj)

    async def delete(self, id: str) -> None:
        self._data.pop(id, None)
