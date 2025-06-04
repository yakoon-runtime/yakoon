from dataclasses import dataclass, field
from typing import Any

@dataclass
class SessionData:
    """
    A grouped key-value store that supports nested access via key paths.
    Group names are explicit (e.g., "system", "realm").
    """

    _store: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_row(self) -> dict:
        return self._store

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj._store = data
        return obj

    def get(self, group: str, path: str, default: Any = None) -> Any:
        """
        Retrieves a value from a nested key path within a group.
        Example: get("realm", "char.id") → returns realm["char"]["id"]
        """
        data = self._store.get(group, {})
        parts = path.split(".")

        for part in parts:
            if not isinstance(data, dict):
                return default
            data = data.get(part, default)
        return data

    def set(self, group: str, path: str, value: Any) -> None:
        """
        Sets a value within a nested key path inside a group.
        Example: set("realm", "char.id", "abc") → realm["char"]["id"] = "abc"
        """
        root = self._store.setdefault(group, {})
        node = root
        parts = path.split(".")

        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
        self._store[group] = root  # ensure update

    def rem(self, group: str, path: str) -> None:
        """
        Removes a key from a nested path inside a group.
        If any level is missing, does nothing.
        """
        node = self._store.get(group)
        parts = path.split(".")

        for part in parts[:-1]:
            if not isinstance(node, dict) or part not in node:
                return
            node = node[part]

        if isinstance(node, dict):
            node.pop(parts[-1], None)

    def group(self, group: str) -> dict[str, Any]:
        return self._store.setdefault(group, {})

    def __getitem__(self, group: str) -> dict[str, Any]:
        return self._store[group]

    def __repr__(self) -> str:
        return f"<SessionData {self._store}>"
