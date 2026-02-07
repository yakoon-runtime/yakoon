from __future__ import annotations
from typing import Optional

from yakoon.kivy.host.context import ViewContext
from yakoon.kivy.pages.tab_overview_page import TabOverviewPage


class AppController:
    """
    UI-Router: bekommt ViewContext (UI-Thread) und leitet an die richtige Page/Widget-Region weiter.
    Später: Tabs, Channels, Regions, neue Windows, etc.
    """

    def __init__(self, app_root):
        self.app_root = app_root
        self.app_root.set_controller(self)

        self.tabs = []
        self.pages = {}
        self.active_tab_id = None
        self._tab_counter = 0

    def set_runner(self, runner):
        self.runner = runner

    def new_chat_tab(self, select: bool = True):
        self._tab_counter += 1
        tab_id = f"chat-{self._tab_counter}"
        title = "chat" if self._tab_counter == 1 else f"chat {self._tab_counter}"

        # neue Page/Widget Instanz
        chat_page = self._create_chat_page()

        self.tabs.append({"id": tab_id, "title": title})
        self.pages[tab_id] = chat_page

        if select or self.active_tab_id is None:
            self.select_tab(tab_id)

        self.app_root.render_tabs(self.tabs, self.active_tab_id)
        return tab_id

    def _create_chat_page(self):
        # du nutzt aktuell ChatWidget – das ist okay als “page content”
        from yakoon.kivy.widgets.chat_widget import ChatWidget
        w = ChatWidget()
        w.runner = self.runner

        # runner injecten (wenn global/shared)
        if hasattr(self.app_root, "runner") and self.app_root.runner:
            w.runner = self.app_root.runner
        return w

    def select_tab(self, tab_id: str):
        if tab_id not in self.pages:
            return
        self.active_tab_id = tab_id
        self.app_root.render_tabs(self.tabs, self.active_tab_id)

        content = self.app_root.ids.content
        content.clear_widgets()
        content.add_widget(self.pages[tab_id])
    
        if hasattr(self.pages[tab_id], "focus_prompt"):
            self.pages[tab_id].focus_prompt()

   
    def dispatch_context(self, ctx: ViewContext) -> None:

        # route output to active page
        page = self.pages.get(self.active_tab_id)
        if page:
            page.apply_context(ctx)

        # 1) App-weite Signals (optional, aber praktisch)
        if getattr(ctx.session, "has_signal", None) and ctx.session.has_signal("exit_app"):
            # AppRoot kann das abfangen (oder hier direkt App.stop)
            if hasattr(self.app_root, "stop_app"):
                self.app_root.stop_app()
            return

        # 2) Routing: aktuell nur Chat
        chat_widget = self._get_chat_target()
        if chat_widget:
            chat_widget.apply_context(ctx)

    def _get_chat_target(self) -> Optional[object]:
        # Annahme: AppRootPage hat id: chat
        ids = getattr(self.app_root, "ids", {})
        return ids.get("chat_widget")

    def focus_active(self):
        page = self.pages.get(self.active_tab_id)
        if page and hasattr(page, "focus_prompt"):
            page.focus_prompt()

    def show_overview(self):
        page = TabOverviewPage()
        page.set_controller(self)
        page.render(self.tabs)

        content = self.app_root.ids.content
        content.clear_widgets()
        content.add_widget(page)

    def show_tabs(self):
        # zeigt die aktive Tab-Page wieder
        content = self.app_root.ids.content
        content.clear_widgets()
        content.add_widget(self.pages[self.active_tab_id])

        # fokus
        if hasattr(self.pages[self.active_tab_id], "focus_prompt"):
            self.pages[self.active_tab_id].focus_prompt()

    def close_tab(self, tab_id: str):
        if tab_id not in self.pages:
            return
        # remove
        self.pages.pop(tab_id, None)
        self.tabs = [t for t in self.tabs if t["id"] != tab_id]

        # pick new active if needed
        if self.active_tab_id == tab_id:
            self.active_tab_id = self.tabs[0]["id"] if self.tabs else None
            if self.active_tab_id:
                self.show_tabs()

        self.app_root.render_tabs(self.tabs, self.active_tab_id)
