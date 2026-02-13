import asyncio


class UnresolvedPromptMonitor:
    """
    Periodically checks for unresolved prompts and logs those exceeding a timeout.

    This monitor tracks registered session prompts (e.g. user inputs waiting on completion)
    and reports if any exceed a given threshold duration.

    Intended for development/debugging to detect hanging or stalled sessions.
    """

    _registry: dict[str, tuple[asyncio.Future, float]] = {}
    _task: asyncio.Task | None = None

    check_interval = 10
    zombie_threshold = 60

    @classmethod
    def track(cls, session_id: str, future: asyncio.Future):
        cls._registry[session_id] = (future, asyncio.get_event_loop().time())

    @classmethod
    def untrack(cls, session_id: str):
        cls._registry.pop(session_id, None)

    @classmethod
    def start(cls):
        async def _loop():
            while True:
                now = asyncio.get_event_loop().time()
                for sid, (fut, started) in list(cls._registry.items()):
                    if fut.done():
                        cls.untrack(sid)
                        continue
                    age = now - started
                    if age > cls.zombie_threshold:
                        print(
                            f"[ZOMBIE] Session '{sid}' has unresolved prompt for {int(age)}s."
                        )
                await asyncio.sleep(cls.check_interval)

        if not cls._task:
            cls._task = asyncio.create_task(_loop())

    @classmethod
    def stop(cls):
        if cls._task:
            cls._task.cancel()
            cls._task = None
