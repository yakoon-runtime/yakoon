import asyncio
from typing import Awaitable, Callable

from yakoon.base.runtime.devtools.prompt import UnresolvedPromptMonitor
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings

from enum import StrEnum

class PromptMode(StrEnum):
    NORMAL = "normal"
    SECRET = "secret"


class DialogManager:
    """
    Manages interactive prompts (e.g. via `ask()`), allowing commands to block
    execution until user input is provided.

    Tracks active prompts by session_key using asyncio Futures.
    """

    DEFAULT_TIMEOUT = 30

    _waiting: dict[str, asyncio.Future] = {}
    _timeouts: dict[str, asyncio.Task] = {}
    _modes: dict[str, PromptMode] = {}  # "normal" | "secret"

    @classmethod
    def cleanup(cls, session: Session) -> None:
        """
        Central cleanup for any prompt end state (resolve, cancel, timeout).
        Ensures no prompt-related state leaks across requests.
        """
        session_key = str(session.key)

        fut = cls._waiting.pop(session_key, None)
        # Do NOT cancel fut here by default - cleanup is used by both resolve/cancel/timeout.
        # Cancel is done explicitly by the caller when needed.

        task = cls._timeouts.pop(session_key, None)
        if task:
            task.cancel()

        cls._modes.pop(session_key, None)

        if settings.base.dev_mode:
            # safe to call even if not tracked
            UnresolvedPromptMonitor.untrack(session_key)

    @classmethod
    def set_prompt(
        cls,
        session: Session,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
        mode: PromptMode = PromptMode.NORMAL,
    ):
        """
        Registers a new prompt Future for the given session.

        Args:
            session: The session requesting input.
            timeout: Optional timeout in seconds. If reached, the prompt is cancelled.
            on_timeout: Optional coroutine executed if timeout is reached.
            mode: "normal" or "secret" (used by hosts to decide echo behavior).

        Returns:
            asyncio.Future: The Future to be awaited by the caller.
        """
        session_key = str(session.key)
        fut = asyncio.get_running_loop().create_future()

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.track(session_key, fut)

        cls._waiting[session_key] = fut
        cls._modes[session_key] = mode

        timeout = timeout or settings.network.prompt_timed_out or cls.DEFAULT_TIMEOUT
        if timeout:
            async def auto_expire():
                await asyncio.sleep(timeout)

                if not fut.done():
                    # Ensure all prompt state is cleaned consistently
                    cls.cleanup(session)
                    fut.cancel()

                    if on_timeout:
                        await on_timeout()
                    else:
                        await session.fail("Prompt timed out.")

            task = asyncio.create_task(auto_expire())
            cls._timeouts[session_key] = task

        return fut

    @classmethod
    def is_waiting(cls, session: Session) -> bool:
        session_key = str(session.key)
        return session_key in cls._waiting

    @classmethod
    def get_mode(cls, session: Session) -> PromptMode:
        """
        Returns the input mode for the currently waiting prompt.
        Defaults to "normal".
        """
        session_key = str(session.key)
        return cls._modes.get(session_key, PromptMode.NORMAL)

    @classmethod
    def resolve_prompt(cls, session: Session, value: str) -> bool:
        session_key = str(session.key)
        fut = cls._waiting.get(session_key)

        if fut and not fut.done():
            # cleanup before setting result to avoid races with timeout task
            cls.cleanup(session)
            fut.set_result(value)
            return True

        # If it's already done or missing, ensure we don't leak mode
        cls._modes.pop(session_key, None)
        return False

    @classmethod
    def cancel_prompt(cls, session: Session) -> None:
        """
        Cancels a prompt manually (e.g. on disconnect).
        """
        session_key = str(session.key)
        fut = cls._waiting.get(session_key)

        # cleanup first (cancel timeout, untrack, remove mode)
        cls.cleanup(session)

        if fut and not fut.done():
            fut.cancel()
