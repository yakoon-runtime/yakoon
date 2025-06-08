from abc import ABC
from typing import Any, Optional
import copy

from yakoon.models.key import Key
from yakoon.models.namespace import Namespace
from yakoon.stores.base.base_store import BaseStore


class MemoryStore(BaseStore):
    """
    In-memory implementation of the Store interface.
    Used for testing and ephemeral session data.
    """

    def __init__(self):
        self._rows: dict[str, dict] = {}  # key = str(Key)

    async def get_by_key(self, key: Key) -> Optional[dict]:
        return copy.deepcopy(self._rows.get(str(key)))

    async def fetch_by_namespace(self, namespace: Namespace, *, limit: int = 100) -> list[dict]:
        scope = namespace.to_str()
        return [
            copy.deepcopy(obj)
            for key_str, obj in self._rows.items()
            if obj.get("__scope__") == scope
        ][:limit]

    async def fetch_by_fields(
        self,
        *,
        namespace: Namespace,
        limit: int = 100,
        **fields: Any
    ) -> list[dict]:
        scope = namespace.to_str()
        return [
            copy.deepcopy(obj)
            for obj in self._rows.values()
            if obj.get("__scope__") == scope and all(obj.get(k) == v for k, v in fields.items())
        ][:limit]

    async def save(self, obj: dict) -> None:
        key_str = obj["__key__"]
        self._rows[key_str] = copy.deepcopy(obj)

    async def delete_by_key(self, key: Key) -> None:
        self._rows.pop(str(key), None)
