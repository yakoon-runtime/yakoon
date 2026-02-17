from dataclasses import dataclass
from typing import Any

DispatchPayload = str | dict[str, Any]


@dataclass(frozen=True)
class DispatchInput:
    payload: DispatchPayload
    batch_id: str | None = None
