from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OutputEvent:
    """Structured output envelope for multi-client rendering.

    Attributes:
        payload: Structured payload to render (e.g. MessageSpec dict).
        mime: MIME type of the payload (e.g., "application/yakoon.message+json").
        channel: Target channel (e.g., "main", "debug", "error", or "audit").
        op: Operation type ("append" or "replace").
        region: Target region ("output", "prompt", or "status").
        meta: Additional metadata as key-value pairs.
    """

    payload: Any
    mime: str = "application/yakoon.message+json"
    channel: str = "main"
    op: str = "append"
    region: str = "output"
    meta: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_payload(payload: Any, **meta: Any) -> "OutputEvent":
        """Creates an OutputEvent from a structured payload."""
        return OutputEvent(payload=payload, meta=meta)

    def with_meta(self, extra: Mapping[str, Any]) -> "OutputEvent":
        """Returns a new OutputEvent with merged metadata.

        Args:
            extra: Additional metadata to merge.

        Returns:
            A new OutputEvent with updated metadata.
        """
        merged = dict(self.meta)
        merged.update(extra)
        return OutputEvent(
            payload=self.payload,
            mime=self.mime,
            channel=self.channel,
            op=self.op,
            region=self.region,
            meta=merged,
        )
