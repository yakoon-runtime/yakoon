# yakoon/kivy/pages/tab_overview_page.py
from __future__ import annotations
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty


class TabOverviewPage(BoxLayout):

    title = StringProperty("Tabs")
    tab_count = NumericProperty(0)
    controller = ObjectProperty(allownone=True)

    def set_controller(self, controller):
        self.controller = controller

    def render(self, tabs):
        self.tab_count = len(tabs)
        grid = self.ids.grid
        grid.clear_widgets()
        for t in tabs:
            card = self._make_card(t["id"], t["title"])
            grid.add_widget(card)

    def _make_card(self, tab_id: str, title: str):
        from kivy.factory import Factory
        card = Factory.TabCard()
        card.tab_id = tab_id
        card.title = title

        card.bind(on_open=lambda _w, tab_id: self._open(tab_id))
        card.bind(on_close=lambda _w, tab_id: self._close(tab_id))

        return card

    def _open(self, tab_id: str):
        if self.controller:
            self.controller.select_tab(tab_id)
            self.controller.show_tabs()

    def _close(self, tab_id: str):
        if self.controller:
            self.controller.close_tab(tab_id)

        # Grid neu aufbauen -> update cards
        self.render(self.controller.tabs)

    def on_new_tab(self):
        if self.controller:
            tab_id =self.controller.new_chat_tab(select=True)
            self._open(tab_id)
            # optional: in overview bleiben oder direkt zurück:
            #self.controller.show_overview()


from kivy.factory import Factory
Factory.register("TabOverviewPage", cls=TabOverviewPage)
