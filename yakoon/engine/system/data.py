from dataclasses import dataclass
from typing import Any

@dataclass
class RuntimeSessionData:
    pass


class StorageSessionData:
    """
    A grouped key-value store that behaves like a nested dict.
    Allows get/set access via (group, key) without raising errors.
    """

    def __init__(self):
        self._store: dict[str, dict[str, Any]] = {}

    def get(self, group: str, key: str, default: Any = None) -> Any:
        return self._store.get(group, {}).get(key, default)

    def set(self, group: str, key: str, value: Any) -> None:
        self._store.setdefault(group, {})[key] = value

    def group(self, group: str) -> dict[str, Any]:
        return self._store.setdefault(group, {})

    def __getitem__(self, group: str) -> dict[str, Any]:
        return self._store[group]

    def __repr__(self) -> str:
        return f"<StorageSessionData {self._store}>"
