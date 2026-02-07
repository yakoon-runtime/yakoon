from __future__ import annotations
from typing import Optional

from yakoon.kivy.host.context import ViewContext


class AppController:
    """
    UI-Router: bekommt ViewContext (UI-Thread) und leitet an die richtige Page/Widget-Region weiter.
    Später: Tabs, Channels, Regions, neue Windows, etc.
    """

    def __init__(self, app_root):
        self.app_root = app_root

    def dispatch_context(self, ctx: ViewContext) -> None:

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
