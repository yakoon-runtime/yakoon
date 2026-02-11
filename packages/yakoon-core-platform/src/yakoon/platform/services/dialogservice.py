import asyncio
from typing import Awaitable, Callable

from yakoon.base.models.prompt import PromptMode
from yakoon.base.runtime.devtools.prompt import UnresolvedPromptMonitor
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings


class DefaultDialogService:
    """
    Manages interactive prompts (e.g. via `ask()`), allowing commands to block
    execution until user input is provided.

    Tracks active prompts by session_key using asyncio Futures.
    """

    DEFAULT_TIMEOUT = 60 * 15
    # Default 15 Minutes

    def __init__(self):
        self._waiting: dict[str, asyncio.Future] = {}   # TODO cleanup
        self._timeouts: dict[str, asyncio.Task] = {}    # TODO cleanup
        self._edges: dict[str, asyncio.Event] = {}      # TODO cleanup
        self._modes: dict[str, PromptMode] = {}         # TODO cleanup

    def edge_event(self, session: Session) -> asyncio.Event:
        """
        Returns an event that is set whenever the prompt state changes for this session.
        Engine can wait on this to avoid polling.
        """
        session_key = str(session.key)
        ev = self._edges.get(session_key)
        if ev is None:
            ev = asyncio.Event()
            self._edges[session_key] = ev
        return ev

    def cleanup(self, session: Session) -> None:
        """
        Central cleanup for any prompt end state (resolve, cancel, timeout).
        Ensures no prompt-related state leaks across requests.
        """
        session_key = str(session.key)

        fut = self._waiting.pop(session_key, None)
        # Do NOT cancel fut here by default - cleanup is used by both resolve/cancel/timeout.
        # Cancel is done explicitly by the caller when needed.

        task = self._timeouts.pop(session_key, None)
        if task:
            task.cancel()

        self._modes.pop(session_key, None)

        if settings.base.dev_mode:
            # safe to call even if not tracked
            UnresolvedPromptMonitor.untrack(session_key)

        # signal: prompt state changed (resolve/cancel/timeout/cleanup)
        self.edge_event(session).set()

    def set_prompt(
        self,
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

        self._waiting[session_key] = fut
        self._modes[session_key] = mode

        # signal: prompt opened
        self.edge_event(session).set()

        timeout = timeout or settings.network.prompt_timed_out or self.DEFAULT_TIMEOUT
        if timeout:
            async def auto_expire():
                await asyncio.sleep(timeout)

                if not fut.done():
                    # Ensure all prompt state is cleaned consistently
                    self.cleanup(session)
                    fut.cancel()

                    if on_timeout:
                        await on_timeout()
                    else:
                        await session.fail("Prompt timed out.")

            task = asyncio.create_task(auto_expire())
            self._timeouts[session_key] = task

        return fut

    def is_waiting(self, session: Session) -> bool:
        session_key = str(session.key)
        return session_key in self._waiting

    def get_mode(self, session: Session) -> PromptMode:
        """
        Returns the input mode for the currently waiting prompt.
        Defaults to "normal".
        """
        session_key = str(session.key)
        return self._modes.get(session_key, PromptMode.NORMAL)

    def resolve_prompt(self, session: Session, value: str) -> bool:
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        if fut and not fut.done():
            # cleanup before setting result to avoid races with timeout task
            self.cleanup(session)
            fut.set_result(value)
            # signal: prompt resolved
            self.edge_event(session).set()  
            return True

        # If it's already done or missing, ensure we don't leak mode
        self._modes.pop(session_key, None)
        return False

    def cancel_prompt(self, session: Session) -> None:
        """
        Cancels a prompt manually (e.g. on disconnect).
        """
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        # cleanup first (cancel timeout, untrack, remove mode)
        self.cleanup(session)

        if fut and not fut.done():
            fut.cancel()
            self.edge_event(session).set()  # signal: prompt cancelled
