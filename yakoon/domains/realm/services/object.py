
from typing import Optional

from yakoon.domains.realm.models.object import Object
from yakoon.domains.realm.stores.memory.object import InMemoryObjectStore


class ObjectService:

    store = InMemoryObjectStore()

    @classmethod
    def get_by_id(cls, obj_id: str) -> Optional[Object]:
        return cls.store.get_by_id(obj_id)

    @classmethod
    def contents_of(cls, location_id: str) -> list[Object]:
        return cls.store.contents_of(location_id)
