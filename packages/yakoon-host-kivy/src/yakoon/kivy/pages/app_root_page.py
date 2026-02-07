
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty


class AppRootPage(BoxLayout):

    sidebar_width = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.controller = None  # wird von app.py gesetzt

    def set_controller(self, controller):
        self.controller = controller

    def on_kv_post(self, base_widget):

        print("AppRootPage ids:", self.ids.keys())
        
        # wird aufgerufen, wenn KV + IDs vollständig gebaut sind
        ##Clock.schedule_once(self._focus_initial, 0)

    # Topbar actions (placeholders)
    def on_right_action_1(self): ...
    def on_right_action_2(self): App.get_running_app().stop()

    def toggle_sidebar(self):
        self.sidebar_width = dp(220) if self.sidebar_width == 0 else 0

    def on_new_tab(self):
        if self.controller:
            tab_id = self.controller.new_chat_tab(select=True)  # muss tab_id zurückgeben
            self.controller.select_tab(tab_id)
            self.controller.show_tabs()

    # Tabs rendering
    def render_tabs(self, tabs, active_id: str):
        area = self.ids.tabs_area
        area.clear_widgets()
        for t in tabs:
            b = self._make_tab_button(t["id"], t["title"], t["id"] == active_id)
            area.add_widget(b)

    def _make_tab_button(self, tab_id: str, title: str, active: bool):
        from kivy.factory import Factory
        btn = Factory.TabPill() # TabButton()
        btn.tab_id = tab_id
        btn.text = title
        btn.active = active
        btn.bind(on_release=lambda *_: self._select_tab(tab_id))
        return btn

    def _select_tab(self, tab_id: str):
        if self.controller:
            self.controller.select_tab(tab_id)

    def focus_initial(self):
        if self.controller:
            self.controller.focus_active()

    def stop_app(self):
        App.get_running_app().stop()

    def on_right_action_1(self):
        if self.controller:
            self.controller.show_overview()


    def on_touch_down(self, touch): 
        sv = self.ids.get("tabs_scroll")
        if sv and sv.collide_point(*touch.pos):
            if touch.button == "scrollup":
                sv.scroll_x = min(1.0, sv.scroll_x + 0.08)
                return True
            if touch.button == "scrolldown":
                sv.scroll_x = max(0.0, sv.scroll_x - 0.08)
                return True
        return super().on_touch_down(touch)