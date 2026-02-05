# yakoon/platform/io/output.py
from __future__ import annotations

import inspect
from dataclasses import asdict
from typing import Any, Awaitable, Callable, Protocol, Union

from yakoon.base.runtime.output.event import OutputEvent


def ensure_async(fn: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    if inspect.iscoroutinefunction(fn):
        return fn  # type: ignore[return-value]

    async def _wrapped(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    return _wrapped


OutputPayload = Union[str, OutputEvent]


class Output(Protocol):
    async def out(self, payload: OutputPayload) -> None: ...
    async def err(self, payload: OutputPayload) -> None: ...


class DefaultOutput:
    """
    Generic output adapter: accepts str | OutputEvent and forwards it.
    Inject concrete sinks (console/ws/telnet) via out_fn/err_fn.
    """

    def __init__(self, out_fn=print, err_fn=print):
        self._out_fn = ensure_async(out_fn)
        self._err_fn = ensure_async(err_fn)

    async def out(self, payload: OutputPayload) -> None:
        await self._out_fn(self._normalize(payload))

    async def err(self, payload: OutputPayload) -> None:
        # If caller gives str, we mark it as error automatically.
        if isinstance(payload, str):
            payload = OutputEvent(text=payload, channel="error", region="status")
        await self._err_fn(self._normalize(payload))

    @staticmethod
    def _normalize(payload: OutputPayload) -> OutputEvent:
        return payload if isinstance(payload, OutputEvent) else OutputEvent(text=payload)

    @staticmethod
    def to_json(payload: OutputPayload) -> dict[str, Any]:
        evt = payload if isinstance(payload, OutputEvent) else OutputEvent(text=payload)
        return asdict(evt)
