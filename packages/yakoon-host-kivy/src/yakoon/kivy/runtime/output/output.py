from yakoon.base.runtime.output.event import OutputEvent
from yakoon.kivy.runtime.context.view_context import ViewContext
from yakoon.platform.output.default import DefaultOutput


class KivyOutput:

    def __init__(self, on_context, ui_state_provider):
        self._on_context = on_context
        self._ui_state_provider = ui_state_provider

    def emit(self, session, evt: OutputEvent):
        ctx = ViewContext(
            session=session, envelope=evt, ui_state_provider=self._ui_state_provider
        )
        self._on_context(ctx)


class SessionBoundKivyOutput(DefaultOutput):

    def __init__(self, session, kivy_output: KivyOutput):
        super().__init__(
            out_fn=lambda evt: kivy_output.emit(session, evt),
            err_fn=lambda evt: kivy_output.emit(session, evt),
        )
