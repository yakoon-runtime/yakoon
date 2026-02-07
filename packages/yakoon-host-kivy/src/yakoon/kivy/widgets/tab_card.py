
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivy.clock import Clock


class TabCard(ButtonBehavior, BoxLayout):

    tab_id = StringProperty("")
    title = StringProperty("")

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self._suppress_open = False
        self.register_event_type("on_open")
        self.register_event_type("on_close")

    def on_open(self, *args): pass
    def on_close(self, *args): pass

    def open(self):
        self.dispatch("on_open", self.tab_id)

    def close(self):
        # verhindert, dass der Card-Release nach dem Button-Release "open" triggert
        self._suppress_open = True
        Clock.schedule_once(lambda _dt: setattr(self, "_suppress_open", False), 0)

        self.dispatch("on_close", self.tab_id)

    def on_release(self):
        if self._suppress_open:
            return
        self.dispatch("on_open", self.tab_id)