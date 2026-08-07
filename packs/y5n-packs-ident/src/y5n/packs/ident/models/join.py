from __future__ import annotations

from dataclasses import dataclass, field

from y5n.runtime.api.naming import Key, Namespace
from y5n.runtime.store.event import GetResult


@dataclass
class JoinData:

    CURRENT_VERSION = 1

    account_key: Key
    group_key: Key

    enabled: bool = True

    _v: int = field(default=CURRENT_VERSION)

    def is_active(self) -> bool:
        return self.enabled

    def to_dict(self) -> dict:
        return {
            "account_key": str(self.account_key),
            "group_key": str(self.group_key),
            "enabled": self.enabled,
            "_v": self._v,
        }

    @classmethod
    def from_dict(cls, d: dict) -> JoinData:
        d = dict(d or {})

        return cls(
            account_key=Key.from_str(d["account_key"]),
            group_key=Key.from_str(d["group_key"]),
            enabled=d.get("enabled", True),
            _v=d.get("_v", 0),
        )


class Join:
    def __init__(self, key: Key, data: JoinData):
        self.key = key
        self.data = data

    @staticmethod
    def build_key(*, namespace: Namespace, account_key: Key, group_key: Key) -> Key:
        return Key(namespace=namespace, id=f"{group_key}:{account_key}")

    @property
    def account_key(self) -> Key:
        return self.data.account_key

    @property
    def group_key(self) -> Key:
        return self.data.group_key

    def is_active(self) -> bool:
        return self.data.is_active()

    @classmethod
    def from_row(cls, row: GetResult) -> Join:
        data = row.require_object()
        return cls(
            key=row.key,
            data=JoinData.from_dict(data),
        )
