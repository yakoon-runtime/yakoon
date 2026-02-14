import asyncio
from collections.abc import Awaitable, Callable

from yakoon.base.models.fields import FieldSpec, FormSpec
from yakoon.base.ports import DialogState, DialogValue
from yakoon.base.runtime.devtools.prompt import UnresolvedPromptMonitor
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings


class DefaultDialogService:
    """
    Manages interactive input in two shapes:

    - Wizard mode: requests exactly ONE FieldSpec and resolves with a single value
    - Form mode:   requests a FormSpec (list of fields) and resolves with dict values

    The Runner uses DialogState to decide whether to collect:
      - wizard input (single field)
      - form input (FormSpec)
    """

    DEFAULT_TIMEOUT = 60 * 15  # 15 minutes

    def __init__(self):
        # One future per session; resolves to DialogValue (single value OR dict of values)
        self._waiting: dict[str, asyncio.Future] = {}  # TODO cleanup
        self._timeouts: dict[str, asyncio.Task] = {}  # TODO cleanup
        self._edges: dict[str, asyncio.Event] = {}  # TODO cleanup

        self._states: dict[str, DialogState] = {}  # TODO cleanup

        self._field_specs: dict[str, FieldSpec] = {}  # TODO cleanup
        self._form_specs: dict[str, FormSpec] = {}  # TODO cleanup

    def state(self, session: Session) -> DialogState:
        session_key = str(session.key)
        return self._states.get(session_key, DialogState.IDLE)

    def is_waiting(self, session: Session) -> bool:
        session_key = str(session.key)
        return session_key in self._waiting

    def edge_event(self, session: Session) -> asyncio.Event:
        session_key = str(session.key)
        ev = self._edges.get(session_key)
        if ev is None:
            ev = asyncio.Event()
            self._edges[session_key] = ev
        return ev

    def get_field_spec(self, session: Session) -> FieldSpec:
        session_key = str(session.key)
        spec = self._field_specs.get(session_key)
        if spec is None:
            raise RuntimeError("No field spec available (not in WAITING_WIZARD).")
        return spec

    def wait_field(
        self,
        session: Session,
        *,
        field: FieldSpec,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
    ) -> asyncio.Future:
        """
        Register a wizard request for exactly ONE field.
        The future resolves with a single field value (DialogValue = object).
        """
        return self._set_waiting(
            session,
            state=DialogState.WAITING_WIZARD,
            timeout=timeout,
            on_timeout=on_timeout,
            field_spec=field,
            form_spec=None,
        )

    def get_form_spec(self, session: Session) -> FormSpec:
        session_key = str(session.key)
        spec = self._form_specs.get(session_key)
        if spec is None:
            raise RuntimeError("No form spec available (not in WAITING_FORM).")
        return spec

    def wait_form(
        self,
        session: Session,
        *,
        spec: FormSpec,
        timeout: float | None = None,
        on_timeout: Callable[[], Awaitable[None]] | None = None,
    ) -> asyncio.Future:
        """
        Register a form request (FormSpec) and block until values are provided.
        The future resolves with dict[str, object].
        """
        return self._set_waiting(
            session,
            state=DialogState.WAITING_FORM,
            timeout=timeout,
            on_timeout=on_timeout,
            field_spec=None,
            form_spec=spec,
        )

    def resolve_input(self, session: Session, value: DialogValue) -> bool:
        """
        Resolve the currently waiting dialog (wizard or form).

        - Wizard: a single value (object)
        - Form:   dict[str, object]
        """
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        if fut and not fut.done():
            # cleanup before setting result to avoid races with timeout task
            self.cleanup(session)
            fut.set_result(value)
            self.edge_event(session).set()
            return True

        # Ensure we don't leak state if resolution is late/invalid
        self._states.pop(session_key, None)
        self._form_specs.pop(session_key, None)
        self._field_specs.pop(session_key, None)
        return False

    def cancel_input(self, session: Session) -> None:
        session_key = str(session.key)
        fut = self._waiting.get(session_key)

        self.cleanup(session)

        if fut and not fut.done():
            fut.cancel()
            self.edge_event(session).set()

    def clear(self, session: Session) -> None:
        self.cleanup(session)

    def cleanup(self, session: Session) -> None:
        session_key = str(session.key)

        _ = self._waiting.pop(session_key, None)

        task = self._timeouts.pop(session_key, None)
        if task:
            task.cancel()

        self._states.pop(session_key, None)
        self._form_specs.pop(session_key, None)
        self._field_specs.pop(session_key, None)

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.untrack(session_key)

        self.edge_event(session).set()

    def _set_waiting(
        self,
        session: Session,
        *,
        state: DialogState,
        timeout: float | None,
        on_timeout: Callable[[], Awaitable[None]] | None,
        field_spec: FieldSpec | None,
        form_spec: FormSpec | None,
    ) -> asyncio.Future:
        session_key = str(session.key)
        fut = asyncio.get_running_loop().create_future()

        if settings.base.dev_mode:
            UnresolvedPromptMonitor.track(session_key, fut)

        self._waiting[session_key] = fut
        self._states[session_key] = state

        if field_spec is not None:
            self._field_specs[session_key] = field_spec
        else:
            self._field_specs.pop(session_key, None)

        if form_spec is not None:
            self._form_specs[session_key] = form_spec
        else:
            self._form_specs.pop(session_key, None)

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
                        await session.fail("Prompt timed out.")

            self._timeouts[session_key] = asyncio.create_task(auto_expire())

        return fut
