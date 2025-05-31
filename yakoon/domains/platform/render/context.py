
from yakoon.runtime.models.session import BaseSession
from yakoon.domains.platform.render.engine.context import RenderContext
from yakoon.domains.platform.render.engine.render import render_section
from yakoon.domains.platform.render.dialog.prompts import Prompts


class Presenter:
    """
    Handles structured, localized output rendering for a command session.

    Wraps the template context and provides high-level methods for emitting
    messages, failures, and notifications using predefined sections in the template.
    """
    
    def __init__(self, template_key: str, session: BaseSession) -> RenderContext:
        """
        Constructs a RenderContext based on the current session and template key.

        Args:
            template_key (str): Relative template path (e.g. 'account/cmd_login').
            session: Session object with language information.

        Returns:
            RenderContext: Template context with full key and language.
        """
        self._prompts = None
        self._session = session
        self._ctx = RenderContext(key=template_key, lang=session.lang)

    @property
    def prompts(self) -> Prompts:
        if not self._prompts:
            self._prompts = Prompts(self._ctx, self._session)
        return self._prompts

    async def emit(self, section: str, **data):
        """
        Renders and emits a section of the current template via session.emit().

        Used for standard informational output (e.g. success, details, confirmations).

        Args:
            section (str): Template section key (e.g. "success", "info").
            **data: Optional key-value pairs for template variables.
        """
        text = render_section(self._ctx, section, **data)
        await self._session.emit(text)

    async def fail(self, section: str, **data):
        """
        Renders and sends a failure message via session.fail().

        Used to communicate errors, invalid inputs, or blocked operations.

        Args:
            section (str): Template section key (e.g. "not_found", "denied").
            **data: Optional key-value pairs for template variables.
        """
        text = render_section(self._ctx, section, **data)
        await self._session.fail(text)

    async def notify(self, section: str, **data):
        """
        Renders and sends a passive notification via session.notify().

        Used for non-critical messages, hints or background updates.

        Args:
            section (str): Template section key (e.g. "hint", "auto_saved").
            **data: Optional key-value pairs for template variables.
        """
        text = render_section(self._ctx, section, **data)
        await self._session.notify(text)





