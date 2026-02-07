
from kivy.clock import Clock
from yakoon.kivy.host.context import ViewContext


class KivyOutput:

    def __init__(self, session, dispatch_context, ui_state_provider=None):
        self._session = session
        self._dispatch_context = dispatch_context
        self._ui_state_provider = ui_state_provider or (lambda: {})

    async def emit(self, envelope):
        ctx = ViewContext(
            session=self._session,
            envelope=envelope,
            ui_state=self._ui_state_provider(),
        )
        Clock.schedule_once(lambda _dt: self._dispatch_context(ctx), 0)
