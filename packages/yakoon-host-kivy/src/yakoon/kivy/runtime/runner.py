import asyncio
import threading
from typing import Optional


class SessionRunner:
    
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._queue: Optional[asyncio.Queue[str]] = None

    def start(self):
        if self._thread:
            return

        self._thread = threading.Thread(target=self._thread_main, daemon=True)
        self._thread.start()

    def _thread_main(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._queue = asyncio.Queue()
        self._loop.create_task(self._run())
        self._loop.run_forever()

    def submit(self, text: str):
        # thread-safe: enqueue in runner loop
        if not self._loop or not self._queue:
            return
        self._loop.call_soon_threadsafe(self._queue.put_nowait, text)

    async def _run(self):
        assert self._queue is not None
        while True:
            text = await self._queue.get()
            await self.engine.dispatch(self.session, text)
            if hasattr(self.session, "has_signal") and self.session.has_signal("exit_app"):
                break
