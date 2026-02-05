# yakoon/host/console/console_output.py
from __future__ import annotations
from typing import Any

from yakoon.base.runtime.output.event import OutputEvent
from yakoon.platform.output.base import DefaultOutput



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
        # Keep it minimal; don't dump meta by default.
        prefix = ""
        if evt.channel != "main":
            prefix += f"[{evt.channel}] "
        if evt.region is "output":
            prefix += f"({evt.region}) "
        if evt.region is "information":
            prefix += f"({evt.region}) "
        if evt.region is "status":
            prefix += f"({evt.region}) "

        return f"{prefix}{evt.text}"
