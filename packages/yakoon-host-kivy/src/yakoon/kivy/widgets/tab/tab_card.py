from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock


class TabCard(ButtonBehavior, BoxLayout):

    tab_id = StringProperty("")
    title = StringProperty("")
    _suppress_open = BooleanProperty(False)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.register_event_type("on_open")
        self.register_event_type("on_close")

    # --- events ----------------------------------------------------------

    def on_open(self, *args):
        pass

    def on_close(self, *args):
        pass

    # --- actions ---------------------------------------------------------

    def open(self):
        if self._suppress_open:
            return
        self.dispatch("on_open", self.tab_id)

    def close(self):
        # verhindert, dass der Card-Release danach noch open triggert
        self._suppress_open = True
        Clock.schedule_once(self._unsuppress, 0)
        self.dispatch("on_close", self.tab_id)

    def _unsuppress(self, _dt):
        self._suppress_open = False

    # --- ButtonBehavior hook --------------------------------------------

    def on_release(self):
        self.open()


from kivy.factory import Factory

Factory.register("TabCard", cls=TabCard)
