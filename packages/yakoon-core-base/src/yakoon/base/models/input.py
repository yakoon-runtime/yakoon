
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DispatchInput:
    command: str
    batch_id: str | None = None


