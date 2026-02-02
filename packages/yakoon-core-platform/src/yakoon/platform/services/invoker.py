
from yakoon.base.runtime.session.session import Session


class CommandInvokerService:
    """
    Executes commands through the normal engine pipeline.
    Used by meta-commands (e.g. batch, aliases) to invoke other commands
    without bypassing routing, permissions, auditing, or rendering.
    """
        
    def __init__(self):
        self._engine = None
        self._max_depth = 10

    def attach(self, engine) -> None:
        if self._engine is not None:
            return RuntimeError("CommandInvokerService already attached")
        self._engine = engine

    async def invoke_text(self, session:Session, text: str) -> bool:

        depth = getattr(session, "_invoke_depth", 0) + 1
        if depth > self._max_depth:
            return False #raise RuntimeError("Max command invocation depth reached")
        setattr(session, "_invoke_depth", depth)
        try:
            return await self._engine.invoke_text(session, text)
        finally:
            setattr(session, "_invoke_depth", depth - 1)