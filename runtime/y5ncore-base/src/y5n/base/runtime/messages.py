"""Runtime Bus message types.

Each message is a dataclass. The bus routes by type.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import auto, StrEnum


class Visibility(StrEnum):
    LOCAL = auto()
    PARENT = auto()
    GLOBAL = auto()


@dataclass
class RegisterProvider:
    provider_id: str
    exports: dict[str, Sequence[str]]
    service: dict | None = None
    visibility: Visibility = Visibility.GLOBAL
    caller_path: str | None = None


@dataclass
class UnregisterProvider:
    provider_id: str


@dataclass
class Ok:
    pass
