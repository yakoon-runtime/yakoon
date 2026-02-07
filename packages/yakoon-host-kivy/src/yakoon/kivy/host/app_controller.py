from __future__ import annotations
from typing import Optional

from yakoon.kivy.host.context import ViewContext
from yakoon.kivy.pages.tab_overview_page import TabOverviewPage
from yakoon.kivy.widgets.chat import ChatWidget


class AppController:
    """
    UI-Router: bekommt ViewContext (UI-Thread) und leitet an die richtige Page/Widget-Region weiter.
    Tabs + Navigation gehören hierher, aber ohne UI-Gewalt (kein clear_widgets() im Normalfall).
    """

    def __init__(self, app_root):
        self.app_root = app_root
        self.app_root.set_controller(self)

        self.tabs: list[dict] = []
        self.pages: dict[str, object] = {}
        self.active_tab_id: Optional[str] = None
        self._tab_counter = 0
        self.runner = None

    def set_runner(self, runner):
        self.runner = runner

    # ---------------------------------------------------------------------
    # Tabs
    # ---------------------------------------------------------------------

    def new_chat_tab(self, select: bool = True) -> str:
        self._tab_counter += 1
        tab_id = f"chat-{self._tab_counter}"
        title = "chat" if self._tab_counter == 1 else f"chat {self._tab_counter}"

        page = self._create_chat_page()
        self.tabs.append({"id": tab_id, "title": title})
        self.pages[tab_id] = page

        if select or self.active_tab_id is None:
            self.select_tab(tab_id)

        self.app_root.render_tabs(self.tabs, self.active_tab_id)
        return tab_id

    def close_tab(self, tab_id: str):
        if tab_id not in self.pages:
            return

        # 1) entfernen
        self.pages.pop(tab_id, None)
        self.tabs = [t for t in self.tabs if t["id"] != tab_id]

        # 2) neuen aktiven Tab wählen, falls nötig
        if self.active_tab_id == tab_id:
            self.active_tab_id = self.tabs[0]["id"] if self.tabs else None
            if self.active_tab_id:
                self.select_tab(self.active_tab_id)
            else:
                # keine Tabs mehr -> optional: Overview zeigen
                if hasattr(self.app_root, "show_screen"):
                    self.app_root.show_screen("overview")

        # 3) Tabs-Leiste aktualisieren
        self.app_root.render_tabs(self.tabs, self.active_tab_id)

        # 4) Overview aktualisieren, falls offen
        overview = getattr(self.app_root, "ids", {}).get("overview_page")
        if overview and hasattr(overview, "render"):
            overview.render(self.tabs)


    def _create_chat_page(self):
        w = ChatWidget()
        w.runner = self.runner
        if hasattr(self.app_root, "runner") and getattr(self.app_root, "runner", None):
            w.runner = self.app_root.runner
        return w

    def select_tab(self, tab_id: str):
        if tab_id not in self.pages:
            return
        self.active_tab_id = tab_id
        self.app_root.render_tabs(self.tabs, self.active_tab_id)

        # ✅ neuer Weg: Tabs-Screen anzeigen + Content in TabViewPage setzen
        if hasattr(self.app_root, "show_screen"):
            self.app_root.show_screen("tabs")

        tabs_page = self._tabs_page()
        if tabs_page and hasattr(tabs_page, "set_content"):
            tabs_page.set_content(self.pages[tab_id])
        else:
            # ↩ Fallback: alter content-container (solange ScreenManager noch nicht in KV ist)
            content = getattr(self.app_root, "ids", {}).get("content")
            if content:
                content.clear_widgets()
                content.add_widget(self.pages[tab_id])

        self.focus_active()

    def focus_active(self):
        page = self.pages.get(self.active_tab_id)
        if page and hasattr(page, "focus_prompt"):
            page.focus_prompt()

    # ---------------------------------------------------------------------
    # Navigation (Overview / Tabs)
    # ---------------------------------------------------------------------

    def show_overview(self):
        # ✅ neuer Weg: Overview-Screen zeigen und existing OverviewPage rendern
        if hasattr(self.app_root, "show_screen"):
            overview = self._overview_page()
            if overview and hasattr(overview, "render"):
                overview.set_controller(self)
                overview.render(self.tabs)
            else:
                # fallback: wenn ScreenManager noch nicht eingebaut ist
                page = TabOverviewPage()
                page.set_controller(self)
                page.render(self.tabs)
                content = getattr(self.app_root, "ids", {}).get("content")
                if content:
                    content.clear_widgets()
                    content.add_widget(page)

            self.app_root.show_screen("overview")
            return

        # ↩ alter Weg (wenn AppRoot noch kein ScreenManager hat)
        page = TabOverviewPage()
        page.set_controller(self)
        page.render(self.tabs)
        content = getattr(self.app_root, "ids", {}).get("content")
        if content:
            content.clear_widgets()
            content.add_widget(page)

    def show_tabs(self):
        if hasattr(self.app_root, "show_screen"):
            self.app_root.show_screen("tabs")
            # active tab content sicherstellen
            if self.active_tab_id:
                tabs_page = self._tabs_page()
                if tabs_page and hasattr(tabs_page, "set_content"):
                    tabs_page.set_content(self.pages[self.active_tab_id])
            self.focus_active()
            return

        # ↩ alter Weg
        if not self.active_tab_id:
            return
        content = getattr(self.app_root, "ids", {}).get("content")
        if content:
            content.clear_widgets()
            content.add_widget(self.pages[self.active_tab_id])
        self.focus_active()

    # ---------------------------------------------------------------------
    # Output routing
    # ---------------------------------------------------------------------

    def dispatch_context(self, ctx: ViewContext) -> None:
        # App-wide signals
        if getattr(ctx.session, "has_signal", None) and ctx.session.has_signal("exit_app"):
            if hasattr(self.app_root, "stop_app"):
                self.app_root.stop_app()
            return

        # ✅ EINZIGES Routing: an aktive Page (kein zweites "chat_widget" Target mehr!)
        page = self.pages.get(self.active_tab_id)
        if page and hasattr(page, "apply_context"):
            page.apply_context(ctx)

    # ---------------------------------------------------------------------
    # Helpers: IDs aus AppRoot/KV (ScreenManager-Variante)
    # ---------------------------------------------------------------------

    def _tabs_page(self) -> Optional[object]:
        ids = getattr(self.app_root, "ids", {})
        return ids.get("tabs_page")

    def _overview_page(self) -> Optional[object]:
        ids = getattr(self.app_root, "ids", {})
        return ids.get("overview_page")
