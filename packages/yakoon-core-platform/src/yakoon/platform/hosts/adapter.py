from __future__ import annotations

from typing import Protocol

from yakoon.base.models.fields import FieldSpec, FormSpec


class HostAdapter(Protocol):
    """
    HostAdapter is the UI boundary.

    Engine -> UI only.
    UI -> Engine goes via Runner callbacks.
    """

    async def on_field(self, *, ps1: str, field: FieldSpec) -> None: ...
    async def on_form(self, *, ps1: str, spec: FormSpec) -> None: ...

    # Idle / ready states
    async def on_ready(self, *, ps1: str) -> None: ...
    async def on_idle(self) -> None: ...
    async def on_exit(self) -> None: ...
