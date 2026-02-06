
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class AppRootPage(BoxLayout):

    def on_kv_post(self, base_widget):

        print("AppRootPage ids:", self.ids.keys())
        
        # wird aufgerufen, wenn KV + IDs vollständig gebaut sind
        Clock.schedule_once(self._focus_initial, 0)

    def _focus_initial(self, _dt):
        chat = self.ids.get("chat_widget")
        if chat and hasattr(chat, "prompt"):
            chat.prompt.focus_input()