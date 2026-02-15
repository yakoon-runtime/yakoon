import asyncio
from collections.abc import Awaitable, Callable

from yakoon.base.models.fields import FormSpec
from yakoon.base.ports import DialogState
from yakoon.base.runtime.devtools.prompt import UnresolvedPromptMonitor
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings


class DefaultDialogService:
    """
    Unified input dialog service.

    There is exactly one interactive shape:
      - WAITING_INPUT → FormSpec (1..n fields)
      - resolve_input() → dict[str, object]

    A single-field "wizard" is just a FormSpec with one field.
    """

    DEFAULT_TIMEOUT = 60 * 15  # 15 minutes

    def __init__(self):
        self._waiting: dict[str, asyncio.Future] = {}
        self._timeouts: dict[str, asyncio.Task] = {}
        self._edges: dict[str, asyncio.Event] = {}
        self._states: dict[str, DialogState] = {}
        self._form_specs: dict[str, FormSpec] = {}

    # -----------------------------------------------------
    # State
    # -----------------------------------------------------

    def state(self, session: Session) -> DialogState:
        return self._states.get(str(session.key), DialogState.IDLE)

    def is_waiting(self, session: Session) -> bool:
        return str(session.key) in self._waiting

    def edge_event(self, session: Session) -> asyncio.Event:
        session_key = str(session.key)
        ev = self._edges.get(session_key)
        if ev is None:
            ev = asyncio.Event()
            self._edges[session_key] = ev
        return ev

    # -----------------------------------------------------
    # Input registration
    # -----------------------------------------------------

    def get_form_spec(self, session: Session) -> FormSpec:
        spec = self._form_specs.get(str(session.key))
        if spec is None:
            raise RuntimeError("No FormSpec available (not in WAITING_INPUT).")
        return spec

    def wait_input(
        self,
        session: Session,
        *,
        spec: FormSpec,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
    ) -> asyncio.Future:
        """
        Register an input request (FormSpec).
        Future resolves with dict[str, object].
        """
        return self._set_waiting(
            session=session,
            state=DialogState.WAITING_FORM,  # reuse enum, semantics now unified
            spec=spec,
            timeout=timeout,
            on_timeout=on_timeout,
        )

    # -----------------------------------------------------
    # Resolution
    # -----------------------------------------------------

    def resolve_input(self, session: Session, values: dict[str, object]) -> bool:
        """
        Resolve current input request.
        """
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        if fut and not fut.done():
            self.cleanup(session)
            fut.set_result(values)
            self.edge_event(session).set()
            return True

        self._states.pop(session_key, None)
        self._form_specs.pop(session_key, None)
        return False

    def cancel_input(self, session: Session) -> None:
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        self.cleanup(session)

        if fut and not fut.done():
            fut.cancel()
            self.edge_event(session).set()

    # -----------------------------------------------------
    # Cleanup
    # -----------------------------------------------------

    def cleanup(self, session: Session) -> None:
        session_key = str(session.key)

        _ = self._waiting.pop(session_key, None)

        task = self._timeouts.pop(session_key, None)
        if task:
            task.cancel()

        self._states.pop(session_key, None)
        self._form_specs.pop(session_key, None)

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.untrack(session_key)

        self.edge_event(session).set()

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------

    def _set_waiting(
        self,
        *,
        session: Session,
        state: DialogState,
        spec: FormSpec,
        timeout: float | None,
        on_timeout: Callable[[], Awaitable[None]] | None,
    ) -> asyncio.Future:
        session_key = str(session.key)
        fut = asyncio.get_running_loop().create_future()

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.track(session_key, fut)

        self._waiting[session_key] = fut
        self._states[session_key] = state
        self._form_specs[session_key] = spec

        self.edge_event(session).set()

        timeout = timeout or settings.network.prompt_timed_out or self.DEFAULT_TIMEOUT

        if timeout:

            async def auto_expire():
                await asyncio.sleep(timeout)
                if not fut.done():
                    self.cleanup(session)
                    fut.cancel()
                    if on_timeout:
                        await on_timeout()
                    else:
                        await session.fail("Input timed out.")

            self._timeouts[session_key] = asyncio.create_task(auto_expire())

        return fut
