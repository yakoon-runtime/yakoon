from abc import ABC
from yakoon.models.key import Key
from typing import Any, Optional
import copy

from yakoon.stores.base.base_store import BaseStore
from yakoon.models.namespace import Key, Namespace


class MemoryStore(BaseStore, ABC):
    """
    In-memory implementation of the Store interface.
    Used for testing and ephemeral session data.
    """

    def __init__(self):
        self._rows: dict[str, dict] = {}  # key = str(Key)

    async def get_by_key(self, key: Key) -> Optional[dict]:
        return copy.deepcopy(self._rows.get(str(key)))

    async def fetch_by_namespace(self, namespace: Namespace, *, limit: int = 100) -> list[dict]:
        return [
            copy.deepcopy(obj)
            for obj in self._rows.values()
            if (
                obj.get("_domain") == namespace.domain and
                obj.get("_bucket") == namespace.bucket and
                obj.get("_scope") == namespace.scope
            )
        ][:limit]

    async def fetch_by_fields(self, *, namespace: Namespace, limit: int = 100, **fields: Any) -> list[dict]:
        return [
            copy.deepcopy(obj)
            for obj in self._rows.values()
            if (
                obj.get("_domain") == namespace.domain and
                obj.get("_bucket") == namespace.bucket and
                obj.get("_scope") == namespace.scope and
                all(obj.get(k) == v for k, v in fields.items())
            )
        ][:limit]

    async def save(self, obj: dict) -> None:
        key = Key.from_parts(obj["_domain"], obj["_bucket"], obj["_scope"], obj["_id"])
        self._rows[str(key)] = copy.deepcopy(obj)

    async def delete_by_key(self, key: Key) -> None:
        self._rows.pop(str(key), None)
