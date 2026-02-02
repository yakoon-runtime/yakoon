from collections import deque
from typing import Deque


class CommandQueueService:
    
    def __init__(self):
        self._q: dict[str, Deque[str]] = {}

    def push_front_many(self, session, cmds: list[str]) -> None:
        skey = str(session.key)
        q = self._q.setdefault(skey, deque())
        for c in reversed(cmds):
            q.appendleft(c)

    def pop_next(self, session) -> str | None:
        skey = str(session.key)
        q = self._q.get(skey)
        if not q:
            return None
        cmd = q.popleft()
        if not q:
            self._q.pop(skey, None)
        return cmd

    def has_next(self, session) -> bool:
        q = self._q.get(str(session.key))
        return bool(q)
