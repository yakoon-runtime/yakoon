from dataclasses import dataclass


@dataclass(frozen=True)
class DispatchInput:
    command: str
    batch_id: str | None = None
