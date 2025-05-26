import asyncio
from collections import defaultdict


class OutputBufferManager:
    def __init__(self):
        self._buffers = defaultdict(list)
        self._locks = defaultdict(asyncio.Lock)
        self._flush_events = defaultdict(asyncio.Event)

    async def collect(self, session_id: str, msg: str):
        async with self._locks[session_id]:
            self._buffers[session_id].append(str(msg))
            self._flush_events[session_id].set()

    async def flush_when_ready(self, session_id: str, timeout=1.0) -> str:
        # warte, bis mindestens ein msg geschrieben wurde oder Timeout
        event = self._flush_events[session_id]
        try:
            await asyncio.wait_for(event.wait(), timeout)
        except asyncio.TimeoutError:
            pass
        self._flush_events[session_id].clear()
        return self.flush(session_id)

    def flush(self, session_id: str) -> str:
        return "\n".join(self._buffers.pop(session_id, []))
