
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty


class AppRootPage(BoxLayout):
    sidebar_width = NumericProperty(0)

    # optional: nützlich zum Debuggen / KV-Binding
    current_screen = StringProperty("tabs")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.controller = None  # wird von app.py gesetzt

    def set_controller(self, controller):
        self.controller = controller

    # --- Screen switching -------------------------------------------------

    def show_screen(self, name: str):
        sm = self.ids.get("sm")
        if not sm:
            return
        if sm.current != name:
            sm.current = name
        self.current_screen = name

    def show_tabs(self):
        self.show_screen("tabs")
        # Fokus nach Screenwechsel
        if self.controller:
            self.controller.focus_active()

    def show_overview(self):
        self.show_screen("overview")

    # --- Topbar actions ---------------------------------------------------

    def on_right_action_1(self):
        # Overview öffnen
        if self.controller:
            # Controller soll rendern, Root nur umschalten
            self.controller.show_overview()

    def on_right_action_2(self):
        App.get_running_app().stop()

    def stop_app(self):
        App.get_running_app().stop()

    # --- Sidebar ----------------------------------------------------------

    def toggle_sidebar(self):
        self.sidebar_width = dp(220) if self.sidebar_width == 0 else 0

    # --- Tabs UI: Buttons in der Topbar ----------------------------------

    def on_new_tab(self):
        if self.controller:
            tab_id = self.controller.new_chat_tab(select=True)
            self.controller.select_tab(tab_id)
            # wir zeigen Tabs-Screen (nicht content.clear_widgets)
            self.show_tabs()

    def render_tabs(self, tabs, active_id: str):
        area = self.ids.tabs_area
        area.clear_widgets()
        for t in tabs:
            b = self._make_tab_button(t["id"], t["title"], t["id"] == active_id)
            area.add_widget(b)

    def _make_tab_button(self, tab_id: str, title: str, active: bool):
        from kivy.factory import Factory
        btn = Factory.TabPill()
        btn.tab_id = tab_id
        btn.text = title
        btn.active = active
        btn.bind(on_release=lambda *_: self._select_tab(tab_id))
        return btn

    def _select_tab(self, tab_id: str):
        if self.controller:
            self.controller.select_tab(tab_id)
            self.show_tabs()

    def focus_initial(self):
        if self.controller:
            self.controller.focus_active()

    # --- Mousewheel: nur im Tabs-Screen -----------------------------------

    def on_touch_down(self, touch):
        # Nur im Tabs-Screen das Tab-Scroll-Mausrad abfangen.
        sm = self.ids.get("sm")
        if sm and sm.current != "tabs":
            return super().on_touch_down(touch)

        sv = self.ids.get("tabs_scroll")
        if sv and sv.collide_point(*touch.pos):
            if touch.button == "scrollup":
                sv.scroll_x = min(1.0, sv.scroll_x + 0.08)
                return True
            if touch.button == "scrolldown":
                sv.scroll_x = max(0.0, sv.scroll_x - 0.08)
                return True

        return super().on_touch_down(touch)


from kivy.factory import Factory
Factory.register("AppRootPage", cls=AppRootPage)
