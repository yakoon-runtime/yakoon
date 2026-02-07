
from kivy.clock import Clock
from yakoon.kivy.runtime.context import ViewContext
from yakoon.kivy.models.envelope import Envelope


from typing import Callable, Optional


class KivyOutput:
    def __init__(
        self,
        session,
        on_context: Callable[[object], None],
        ui_state_provider=None,
    ):
        self.session = session
        self._on_context = on_context
        self._ui_state_provider = ui_state_provider

    def emit(self, envelope):
        ctx = ViewContext(
            session=self.session,
            envelope=envelope,
            ui_state=self._ui_state_provider,
        )
        self._on_context(ctx)
