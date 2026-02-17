from __future__ import annotations

from yakoon.base.runtime.output.event import OutputEvent
from yakoon.platform.output.default import DefaultOutput


class ConsoleOutput(DefaultOutput):
    """
    Console renderer (view-only).

    - expects mime: application/yakoon.view+json
    - renders only view.message
    - ignores view.input (handled by Host)
    """

    def __init__(self):
        super().__init__(out_fn=self._print_out, err_fn=self._print_err)

    async def _print_out(self, evt: OutputEvent) -> None:
        text = self._render(evt)
        if text:
            print(text)

    async def _print_err(self, evt: OutputEvent) -> None:
        text = self._render(evt)
        if text:
            print(text)

    def _render(self, evt: OutputEvent) -> str:
        prefix = ""
        if evt.channel != "main":
            prefix += f"[{evt.channel}] "
        if evt.region in {"information", "status"}:
            prefix += f"({evt.region}) "

        # strict: view-only, but still tolerate dict payload if mime mismatches
        payload = evt.payload

        if isinstance(payload, dict) and payload.get("kind") == "view":
            msg = payload.get("message")
            if isinstance(msg, dict):
                return prefix + self._render_message(msg)
            return ""  # input-only views

        # If strictness is desired everywhere, keeping this fallback helps debugging:
        return prefix + str(payload)

    def _render_message(self, spec: dict) -> str:
        lines: list[str] = []

        title = spec.get("title")
        if title:
            lines.append(str(title))
            lines.append("")

        for block in spec.get("blocks", []):
            t = block.get("type")

            if t == "text":
                lines.append(str(block.get("text", "")))
                lines.append("")

            elif t == "list":
                for item in block.get("items", []):
                    lines.append(f"- {item}")
                lines.append("")

            elif t == "kv":
                items = block.get("items", [])
                if isinstance(items, list):
                    for key, value in items:
                        lines.append(f"{key}: {value}")
                lines.append("")

        return "\n".join(lines).rstrip()
