from abc import ABC, abstractmethod
from yakoon.models.key import Key
from typing import Optional, Any


class BaseStore(ABC):
    """
    Abstract base class for all SQL-based object stores.
    Designed for use with PyPika query builders and async drivers like asyncpg or sqlite3.
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[dict]:
        """
        Retrieve an object by its string ID.
        """
        pass

    @abstractmethod
    async def get_by_key(self, key: Key) -> Optional[dict]:
        """
        Retrieve an object using a full typed Key.
        """
        pass

    @abstractmethod
    async def fetch_by_namespace(self, namespace: str, *, limit: int = 100):
        """
        Return all objects within a given namespace.
        """
        pass

    @abstractmethod    
    async def fetch_by_fields(self, *, limit: int = 100, **fields: Any):
        """
        Fetch all objects matching the given field/value pairs.
        Equivalent to a WHERE clause with AND logic.
        """
        pass

    @abstractmethod
    async def save(self, obj: dict) -> None:
        """
        Persist or update the given object. Assumes 'id' or 'key' is present in the dict.
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """
        Delete the object associated with the given string ID.
        """
        pass
