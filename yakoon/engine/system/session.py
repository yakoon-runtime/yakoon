from __future__ import annotations
from typing import Coroutine, Callable, Type, TypeVar
from uuid import uuid4

from typing import TYPE_CHECKING

from yakoon.engine.core.domain.controller import BaseController
if TYPE_CHECKING:
    from yakoon.engine.system.context import Context

Text = TypeVar('Text', str, bytes)
PrintMessage = Callable[[Text], Coroutine]
PrintError = Callable[[Exception], Coroutine]


class BaseSession(object):
    
    out: PrintMessage
    err: PrintError

    def __init__(self, id: str):
        """
        Constructs a new session.
        """
        self.id = id or str(uuid4())
        self._command_groups = []
        self._context = None

    @property
    def ctx(self) -> Context:
        return self._context

    @property
    def command_groups(self) -> list[Type[str]]:
        return self._command_groups
    @command_groups.setter
    def command_groups(self, value):
        self._command_groups = value
    
    def bind_context(self, context: Context):
        self._context = context