from typing import Coroutine, Callable, TypeVar

from engine.runtime.game_context import GameContext
from mygame.models.account import Account
from mygame.models.character import Character

Text = TypeVar('Text', str, bytes)
PrintMessage = Callable[[Text], Coroutine]
PrintError = Callable[[Exception], Coroutine]


class Session(object):
    
    out: PrintMessage
    err: PrintError

    def __init__(self, session_id: str):
        """
        Constructs a new session.
        """
        self.id = session_id
        self._account = Account(id="1", name="Stefan")
        self._character = None # = Character(id="c1", name="Du", location="forest")

    @property
    def ctx(self) -> GameContext:
        return self._context

    @property
    def account(self) -> Account:
        return self._account
    
    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        self._character = value

    def bind_context(self, context: GameContext):
        self._context = context

OnGetSession = Callable[[Session], Coroutine]


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

    async def create_session(self, session_id: str, on_create: OnGetSession):
        """
        Creates a new session by given session_id if session not exists or returns
        the session with given session_id by the event 'on_create'.
        Args:
            session_id: The session id to get or to create.
            on_create: Is called to returns the session.
        Returns:

        """
        if session_id not in self._session:
            self._session[session_id] = Session(session_id)
        self._session[session_id].bind_context(GameContext(self._engine))
        await on_create(self._session[session_id])
