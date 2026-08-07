from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from y5n.runtime.api.naming import Key
from y5n.runtime.store.event import GetResult


@dataclass
class AccountData:

    CURRENT_VERSION = 1

    username: str
    password_hash: str | None = None
    enabled: bool = True

    name: str | None = None
    mail: str | None = None
    language: str | None = None

    data: dict[str, Any] = field(default_factory=dict)

    _v: int = field(default=CURRENT_VERSION)

    def is_active(self) -> bool:
        return self.enabled

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "enabled": self.enabled,
            "name": self.name,
            "mail": self.mail,
            "language": self.language,
            "_v": self._v,
            "data": dict(self.data),
        }

    @classmethod
    def from_dict(cls, d: dict) -> AccountData:
        d = dict(d or {})

        return cls(
            username=d["username"],
            password_hash=d.get("password_hash"),
            enabled=d.get("enabled", True),
            name=d.get("name"),
            mail=d.get("mail"),
            language=d.get("language"),
            data=dict(d.get("data", {})),
            _v=d.get("_v", 0),
        )


class Account:

    def __init__(self, key: Key, data: AccountData):
        self.key = key
        self.data = data

    @property
    def username(self) -> str:
        return self.data.username

    @property
    def name(self) -> str | None:
        return self.data.name

    @property
    def mail(self) -> str | None:
        return self.data.mail

    @property
    def language(self) -> str | None:
        return self.data.language

    def is_active(self) -> bool:
        return self.data.is_active()

    @classmethod
    def from_row(cls, row: GetResult) -> Account:
        data = row.require_object()
        return cls(
            key=row.key,
            data=AccountData.from_dict(data),
        )
