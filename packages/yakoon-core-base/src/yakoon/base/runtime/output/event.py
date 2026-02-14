from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OutputEvent:
    """Minimal output envelope for multi-client rendering.

    Attributes:
        text: The content to render.
        mime: MIME type of the content (e.g., "text/plain" or "text/markdown").
        channel: Target channel (e.g., "main", "debug", "error", or "audit").
        op: Operation type ("append" or "replace").
        region: Target region ("output", "prompt", or "status").
        meta: Additional metadata as key-value pairs.
    """

    text: str
    mime: str = "text/plain"
    channel: str = "main"
    op: str = "append"
    region: str = "output"
    meta: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_text(text: str, **meta: Any) -> OutputEvent:
        """Creates an OutputEvent from plain text.

        Args:
            text: The content to render.
            **meta: Additional metadata as key-value pairs.

        Returns:
            An OutputEvent instance with the given text and metadata.
        """
        return OutputEvent(text=text, meta=meta)

    def with_meta(self, extra: Mapping[str, Any]) -> OutputEvent:
        """Returns a new OutputEvent with merged metadata.

        Args:
            extra: Additional metadata to merge.

        Returns:
            A new OutputEvent with updated metadata.
        """
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
