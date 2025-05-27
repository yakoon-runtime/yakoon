import asyncio


class DialogManager:
    """
    Manages interactive prompts (e.g. via `ask()`), allowing commands to block
    execution until user input is provided.

    This class tracks active prompts using session IDs and resolves them by
    completing stored asyncio Futures. It supports both direct user responses
    (e.g. from console or websocket) and automated resolution within batch flows.
    """

    _waiting: dict[str, asyncio.Future] = {}

    @classmethod
    def set_prompt(cls, session):
        """
        Create and register a new prompt Future for a given session.

        Args:
            session (BaseSession): The session initiating the prompt.

        Returns:
            asyncio.Future: The Future to be awaited by the prompt initiator.
        """         
        fut = asyncio.get_running_loop().create_future()
        cls._waiting[session.id] = fut
        return fut

    @classmethod
    def is_waiting(cls, session_id: str) -> bool:
        """
        Check whether the given session is currently waiting for input.

        Args:
            session_id (str): The ID of the session.

        Returns:
            bool: True if a prompt is active for the session.
        """
        return session_id in cls._waiting

    @classmethod
    def resolve_prompt(cls, session_id: str, value: str) -> bool:
        """
        Resolve the currently active prompt for the session with a given value.

        Args:
            session_id (str): The ID of the session.
            value (str): The user input to fulfill the prompt.

        Returns:
            bool: True if a prompt was resolved; False otherwise.
        """
        fut = cls._waiting.pop(session_id, None)
        if fut and not fut.done():
            fut.set_result(value)
            return True
        return False



