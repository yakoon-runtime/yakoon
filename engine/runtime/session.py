#
# Copyright 2021 The MindCastle Authors. All Rights Reserved.
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# ==============================================================================

import asyncio
from typing import Coroutine, Callable, TypeVar

from engine.data.models.account import Account
from engine.data.models.character import Character

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
        self._account = Account()
        self._character = Character(id="c1", name="Du", location="forest")

    @property
    def character(self) -> Character:
        return self._character

    @property
    def account(self) -> Account:
        return self._account


OnGetSession = Callable[[Session], Coroutine]


class Sessions(object):
    """
    Manages all sessions
    """

    def __init__(self):
        """
        Creates a new instance of class Sessions.
        """
        self._session = {}

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
        await on_create(self._session[session_id])
