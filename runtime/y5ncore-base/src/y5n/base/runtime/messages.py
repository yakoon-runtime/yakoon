"""Runtime Bus message types.

Each message is a dataclass. The bus routes by type.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum, auto


class Placement(StrEnum):
    """Where to register a provider in the tree.

    SELF    → am aufrufenden Node (heutiges provide)
    PARENT  → eine Ebene höher      (heutiges publish)
    ROOT    → systemweit            (heutiges promote)
    """

    SELF = auto()
    PARENT = auto()
    ROOT = auto()


@dataclass
class RegisterProvider:
    provider_id: str
    exports: dict[str, Sequence[str]]
    service: dict | None = None
    placement: Placement = Placement.SELF
    caller_path: str | None = None


@dataclass
class UnregisterProvider:
    provider_id: str


@dataclass
class Ok:
    pass
