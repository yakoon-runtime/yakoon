from __future__ import annotations
from typing import Coroutine, Callable, Type, TypeVar
from uuid import uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.runtime.game_context import GameContext

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

    def update_data(self, source: "BaseSession"):
        self.account = source.account
        self.character = source.character

    @property
    def ctx(self) -> GameContext:
        return self._context

    @property
    def command_groups(self) -> list[Type[str]]:
        return self._command_groups
    @command_groups.setter
    def command_groups(self, value):
        self._command_groups = value
    
    def bind_context(self, context: GameContext):
        self._context = context

OnGetSession = Callable[[BaseSession], Coroutine]


class Sessions(object):
    """
    Manages all sessions
    """

    def __init__(self, engine):
        """
        Creates a new instance of class Sessions.
        """
        self._session = {}
        self._engine = engine

    async def create_session(self, session_id: str, on_create: OnGetSession, on_found: OnGetSession):
        """
        Creates a new session by given session_id if session not exists or returns
        the session with given session_id by the event 'on_create'.
        Args:
            session_id: The session id to get or to create.
            on_create: Is called to returns the session.
        Returns:

        """
        if session_id not in self._session:
            from engine.runtime.game_context import GameContext
            context = GameContext(self._engine)
            session = context.game.session_cls(session_id)
            session.bind_context(context)
            self._session[session_id] = session
            await on_create(self._session[session_id])
        else:
            await on_found(self._session[session_id])