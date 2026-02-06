from kivy.clock import Clock
from yakoon.kivy.host.context import ViewContext


class KivyOutput:
    def __init__(self, session, dispatch_context):
        self._session = session
        self._dispatch_context = dispatch_context

    async def emit(self, envelope):
        ctx = ViewContext(
            session=self._session,
            envelope=envelope,
            ui_state={}
        )
        Clock.schedule_once(lambda _dt: self._dispatch_context(ctx), 0)
