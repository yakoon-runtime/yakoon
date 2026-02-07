from __future__ import annotations
from typing import Optional

from yakoon.kivy.host.context import ViewContext
from yakoon.kivy.controllers.navigator import Navigator
from yakoon.kivy.controllers.tabs_controller import TabsController
from yakoon.kivy.controllers.tabs_overview_controller import OverviewController
from yakoon.kivy.widgets.chat import ChatWidget
from yakoon.kivy.states.tab_state import TabState


class AppController:

    def __init__(self, app_root):

        self.runner = None
        self.app_root = app_root
        self.app_root.set_controller(self)

        # --- STATE ---
        self.tab_state = TabState()

        # --- CONTROLLERS ---
        self.nav = Navigator(app_root)
        self.tabs_ctrl = TabsController(
            app_root, self.nav, self.tab_state)
        self.overview_ctrl = OverviewController(
            app_root, self.nav, self.tabs_ctrl, self.tab_state)

    def set_runner(self, runner):
        self.runner = runner
        self.tabs_ctrl.set_runner(runner)
        self.overview_ctrl.set_runner(runner)

    # --- delegation API (wird von Views/Root benutzt) ---
    def show_overview(self):
        self.overview_ctrl.open()

    def show_tabs(self):
        self.nav.go("tabs")
        self.tabs_ctrl.focus_active()

    def new_chat_tab(self, select: bool = True) -> str:
        return self.tabs_ctrl.new_chat_tab(select=select)

    def select_tab(self, tab_id: str):
        self.tabs_ctrl.select(tab_id)

    def close_tab(self, tab_id: str):
        self.tabs_ctrl.close(tab_id)
        # falls overview offen ist: sinnvoll refreshen
        self.overview_ctrl.refresh()

    # --- output routing ---
    def dispatch_context(self, ctx: ViewContext) -> None:
        if getattr(ctx.session, "has_signal", None) and ctx.session.has_signal("exit_app"):
            if hasattr(self.app_root, "stop_app"):
                self.app_root.stop_app()
            return

        page = self.tabs_ctrl.active_page()
        if page and hasattr(page, "apply_context"):
            page.apply_context(ctx)
