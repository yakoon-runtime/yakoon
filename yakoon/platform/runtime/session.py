
from __future__ import annotations
from yakoon.engine.system.session import BaseSession


class PlatformSession(BaseSession):

    def __init__(self, id: str):
        super().__init__(id)
    