from __future__ import annotations
from typing import Coroutine, Callable, Type, TypeVar
from uuid import uuid4

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yakoon.engine.core.domain.controller import BaseController
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
        self._cmd_groups = []
        self._context:Context = None
        self._domain:BaseController = None

    @property
    def ctx(self) -> Context:
        return self._context

    @property
    def domain(self) -> BaseController:
        return self._domain
    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def cmd_groups(self) -> list[Type[str]]:
        return self._cmd_groups
    @cmd_groups.setter
    def cmd_groups(self, value):
        self._cmd_groups = value
    
    def bind_context(self, context: Context):
        self._context = context

    async def send_msg(self, text: str):
        await self.out(text)

    async def send_status(self, text: str):
        await self.out(f"✅ {text}")

    async def send_error(self, text: str):
        await self.err(f"❌ {text}")

    async def send_cmd(self, input_str: str):
        await self.ctx.send(self, input_str, self.out, self.err)