
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.models.namespace import Namespace


class Key:

    def __init__(self, namespace: Namespace, id: str):
        self.namespace = namespace
        self.id = id

    @staticmethod
    def from_string(raw: str) -> Key:
        parts = raw.split(":")
        if len(parts) != 4:
            raise ValueError(f"Invalid key format: {raw}")
        domain, bucket, scope, id = parts
        from yakoon.models.namespace import Namespace
        return Key(Namespace(domain, bucket, scope), id)
    
    @classmethod
    def from_parts(cls, domain: str, bucket: str, scope: str, id: str) -> "Key":
        from yakoon.models.namespace import Namespace
        return cls(namespace=Namespace(domain, bucket, scope), id=id)

    def to_str(self):
        return str(self)

    def __str__(self):
        return f"{self.namespace.get_prefix()}:{self.id}"

    def __repr__(self):
        return f"<Key {self}>"

    def __eq__(self, other):
        return isinstance(other, Key) and self.namespace == other.namespace and self.id == other.id

    def __hash__(self):
        return hash((self.namespace.get_prefix(), self.id))
    