
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.models.namespace import Namespace

class Key:

    def __init__(self, namespace: Namespace, id_: str):
        self.namespace = namespace
        self.id = id_

    @staticmethod
    def from_string(raw: str) -> Key:
        parts = raw.split(":")
        if len(parts) != 4:
            raise ValueError(f"Invalid key format: {raw}")
        domain, bucket, scope, id_ = parts
        return Key(Namespace(domain, bucket, scope), id_)
    
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
    