from dataclasses import dataclass, field
from typing import Any


@dataclass
class RuntimeSessionData:
    pass


@dataclass
class StorageSessionData:
    """
    A grouped key-value store that behaves like a nested dict.
    Allows get/set access via (group, key) without raising errors.
    """

    # ───── persistent fields (stored in DB/json) ─────

    _store: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return self._store

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj._store = data
        return obj

    def get(self, group: str, key: str, default: Any = None) -> Any:
        """
        Retrieves the value for a key within a specific group.

        Args:
            group (str): The name of the group.
            key (str): The key to look up within the group.
            default (Any): A fallback value if the key or group is not found.

        Returns:
            Any: The stored value, or the default if not found.
        """

        return self._store.get(group, {}).get(key, default)

    def set(self, group: str, key: str, value: Any) -> None:
        """
        Stores a value under the specified key within the given group.

        Args:
            group (str): The name of the group.
            key (str): The key under which the value will be stored.
            value (Any): The value to store.
        """

        self._store.setdefault(group, {})[key] = value

    def rem(self, group: str, key: str) -> None:
        """
        Removes a key from the given group if it exists.
        If the group or key does not exist, nothing happens.
        """
        
        group_data = self._store.get(group)
        if group_data and key in group_data:
            del group_data[key]
            if not group_data:
                del self._store[group]  # optional: clean up empty groups

    def group(self, group: str) -> dict[str, Any]:
        return self._store.setdefault(group, {})

    def __getitem__(self, group: str) -> dict[str, Any]:
        return self._store[group]

    def __repr__(self) -> str:
        return f"<StorageSessionData {self._store}>"
