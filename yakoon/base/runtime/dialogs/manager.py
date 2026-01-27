import asyncio
from typing import Awaitable, Callable

from yakoon.base.runtime.devtools.prompt import UnresolvedPromptMonitor
from yakoon.base.settings import settings


class DialogManager:
    """
    Manages interactive prompts (e.g. via `ask()`), allowing commands to block
    execution until user input is provided.

    This class tracks active prompts using session IDs and resolves them by
    completing stored asyncio Futures. It supports both direct user responses
    (e.g. from console or websocket) and automated resolution within batch flows.
    """

    DEFAULT_TIMEOUT = 30

    _waiting: dict[str, asyncio.Future] = {}
    _timeouts: dict[str, asyncio.Task] = {}
    
    @classmethod
    def set_prompt(cls, session, timeout: float | None = None, on_timeout: Callable[[], Awaitable[None]] | None = None):
        """
        Registers a new prompt Future for the given session.

        Args:
            session: The session requesting input.
            timeout (float | None): Optional timeout in seconds. If reached, the prompt is cancelled.
            on_timeout (Callable | None): Optional coroutine to execute if the timeout is reached.

        Returns:
            asyncio.Future: The Future to be awaited by the caller.
        """
        session_key = str(session.key)
        fut = asyncio.get_running_loop().create_future()

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.track(session_key, fut)

        cls._waiting[session_key] = fut

        # optional timeout auto-cancel
        timeout = timeout or settings.network.prompt_timed_out or cls.DEFAULT_TIMEOUT
        if timeout:
            async def auto_expire():
                await asyncio.sleep(timeout)
                if not fut.done():
                    fut.cancel()
                if on_timeout:
                    await on_timeout()
                else:
                    await session.fail("Prompt timed out.")

            task = asyncio.create_task(auto_expire())
            cls._timeouts[session_key] = task

        return fut

    @classmethod
    def is_waiting(cls, session_key: str) -> bool:
        session_key = str(session_key)
        return session_key in cls._waiting

    @classmethod
    def resolve_prompt(cls, session_key: str, value: str) -> bool:
        session_key = str(session_key)
        fut = cls._waiting.pop(session_key, None)
        if fut and not fut.done():
            # clean up timeout task
            timeout_task = cls._timeouts.pop(session_key, None)
            if timeout_task:
                timeout_task.cancel()
            fut.set_result(value)
            if settings.base.dev_mode:
                UnresolvedPromptMonitor.untrack(session_key)
            return True
        return False

    @classmethod
    def cancel_prompt(cls, session_key: str):
        """
        Cancels a prompt manually (e.g. on disconnect).
        """
        session_key = str(session_key)
        fut = cls._waiting.pop(session_key, None)
        if fut and not fut.done():
            fut.cancel()

        task = cls._timeouts.pop(session_key, None)
        if task:
            task.cancel()
        if settings.base.dev_mode:
            UnresolvedPromptMonitor.untrack(session_key)