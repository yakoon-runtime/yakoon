from __future__ import annotations
from typing import Callable, Optional


class ContextDispatcher:

    def __init__(self):
        self._handler: Optional[Callable[[object], None]] = None

    def set_handler(self, handler: Callable[[object], None]) -> None:
        self._handler = handler

    def __call__(self, ctx) -> None:
        if self._handler:
            self._handler(ctx)
