import asyncio


class ZombieDetector:
    """
    Periodically scans for unresolved prompts and reports potential zombies.
    Intended for development and monitoring purposes only.
    """
    def __init__(self, check_interval=10, zombie_threshold=60):
        self.check_interval = check_interval  # seconds between scans
        self.zombie_threshold = zombie_threshold  # max lifetime in seconds
        self._registry = {}  # session_id -> (Future, start_time)
        self._task = None

    def track(self, session_id: str, future: asyncio.Future):
        self._registry[session_id] = (future, asyncio.get_event_loop().time())

    def untrack(self, session_id: str):
        self._registry.pop(session_id, None)

    async def start(self):
        async def _loop():
            while True:
                now = asyncio.get_event_loop().time()
                for sid, (fut, started) in list(self._registry.items()):
                    if fut.done():
                        self.untrack(sid)
                        continue
                    age = now - started
                    if age > self.zombie_threshold:
                        print(f"[ZOMBIE] Session '{sid}' has unresolved prompt for {int(age)}s.")
                await asyncio.sleep(self.check_interval)

        if not self._task:
            self._task = asyncio.create_task(_loop())

    def stop(self):
        if self._task:
            self._task.cancel()

detector = ZombieDetector()
