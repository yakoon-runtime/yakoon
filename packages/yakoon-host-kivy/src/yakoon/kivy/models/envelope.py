# models/envelope.py
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Envelope:
    text: str
    mime: str = "text/plain"
    channel: str = "main"
    op: str = "append"
    region: str = "output"
    meta: Dict[str, Any] = field(default_factory=dict)
