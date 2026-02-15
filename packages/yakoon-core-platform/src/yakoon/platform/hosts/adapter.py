from __future__ import annotations

from typing import Protocol

from yakoon.base.models.fields import FormSpec


class HostAdapter(Protocol):
    """
    HostAdapter is the UI boundary.

    Engine -> UI only.
    UI -> Engine goes via Runner callbacks.
    """

    async def on_input(self, *, ps1: str, spec: FormSpec) -> None: ...
    async def on_input_submit(self, values: list) -> None: ...

    async def on_ready(self, *, ps1: str) -> None: ...
    async def on_idle(self) -> None: ...
    async def on_exit(self) -> None: ...
