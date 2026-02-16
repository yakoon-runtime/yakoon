from __future__ import annotations

from yakoon.base.runtime.output.event import OutputEvent
from yakoon.platform.output.default import DefaultOutput


class ConsoleOutput(DefaultOutput):
    """
    Console renderer: prints text, optionally prefixes for non-main channels/regions.
    """

    def __init__(self):
        super().__init__(out_fn=self._print_out, err_fn=self._print_err)

    async def _print_out(self, evt: OutputEvent) -> None:
        print(self._render(evt))

    async def _print_err(self, evt: OutputEvent) -> None:
        print(self._render(evt))

    def _render(self, evt: OutputEvent) -> str:
        prefix = ""
        if evt.channel != "main":
            prefix += f"[{evt.channel}] "
        # if evt.region is "output":
        #    prefix += f"({evt.region}) "
        if evt.region == "information":
            prefix += f"({evt.region}) "
        if evt.region == "status":
            prefix += f"({evt.region}) "

        if evt.mime == "application/yakoon.message+json":
            return prefix + self._render_spec(evt.payload)

        # fallback (legacy)
        return prefix + str(evt.payload)

    def _render_spec(self, spec: dict) -> str:
        lines: list[str] = []

        title = spec.get("title")
        if title:
            lines.append(str(title))
            lines.append("")  # blank line

        for block in spec.get("blocks", []):
            t = block.get("type")

            if t == "text":
                lines.append(self._render_inline(block.get("text", "")))
                lines.append("")

            elif t == "list":
                for item in block.get("items", []):
                    lines.append(f"- {self._render_inline(item)}")
                lines.append("")

            elif t == "kv":
                items = block.get("items", [])
                if isinstance(items, list):
                    for key, value in items:
                        lines.append(f"{key}: {value}")
                lines.append("")

        return "\n".join(lines).rstrip()

    def _render_inline(self, value: object) -> str:
        if isinstance(value, str):
            return value

        if isinstance(value, list):
            parts: list[str] = []
            for node in value:
                if not isinstance(node, dict):
                    parts.append(str(node))
                    continue
                t = node.get("type")
                if t == "text":
                    parts.append(str(node.get("text", "")))
                elif t == "code":
                    parts.append(f"`{node.get('code', '')}`")
                elif t == "link":
                    text = node.get("text", "")
                    href = node.get("href", "")
                    parts.append(f"{text} ({href})")
                else:
                    parts.append(str(node))
            return "".join(parts)

        return str(value)
