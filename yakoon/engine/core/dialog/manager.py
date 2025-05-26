import asyncio


class DialogManager:
    _waiting: dict[str, asyncio.Future] = {}

    @classmethod
    def set_prompt(cls, session):
        fut = asyncio.get_event_loop().create_future()
        cls._waiting[session.id] = fut
        return fut

    @classmethod
    def is_waiting(cls, session_id: str) -> bool:
        return session_id in cls._waiting

    @classmethod
    def resolve_prompt(cls, session_id: str, value: str) -> bool:
        fut = cls._waiting.pop(session_id, None)
        if fut and not fut.done():
            fut.set_result(value)
            return True
        return False



