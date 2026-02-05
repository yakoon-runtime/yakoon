# yakoon/base/models/output_event.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class OutputEvent:
    """
    Minimal output envelope for multi-client rendering.
    """
    text: str
    mime: str = "text/plain"          # "text/plain" | "text/markdown"
    channel: str = "main"             # "main" | "debug" | "error" | "audit"
    op: str = "append"                # "append" | "replace"
    region: str = "output"            # "output" | "prompt" | "status"
    meta: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_text(text: str, **meta: Any) -> "OutputEvent":
        return OutputEvent(text=text, meta=meta)

    def with_meta(self, extra: Mapping[str, Any]) -> "OutputEvent":
        merged = dict(self.meta)
        merged.update(extra)
        return OutputEvent(
            text=self.text,
            mime=self.mime,
            channel=self.channel,
            op=self.op,
            region=self.region,
            meta=merged,
        )

