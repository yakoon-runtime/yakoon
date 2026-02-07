
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App


class AppRootPage(BoxLayout):

    def on_kv_post(self, base_widget):

        print("AppRootPage ids:", self.ids.keys())
        
        # wird aufgerufen, wenn KV + IDs vollständig gebaut sind
        Clock.schedule_once(self._focus_initial, 0)


    def focus_initial(self):
        Clock.schedule_once(lambda _dt: self.ids.chat_widget.ids.prompt.focus_input(), 0)

    def stop_app(self):
        App.get_running_app().stop()

    def _focus_initial(self, _dt):
        chat_widget = self.ids.get("chat_widget")
        if chat_widget and hasattr(chat_widget, "prompt"):
            chat_widget.prompt.focus_input()