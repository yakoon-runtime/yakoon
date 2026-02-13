from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.ports import DialogService, PromptService, RendererService
from yakoon.base.runtime.session import Session
from yakoon.platform.runtime.render.context import RenderContext


class PresenterPrompts:
    """
    Provides interactive input methods for user sessions using localized templates.

    This class encapsulates all prompt-based interactions such as text input,
    confirmations, and choices.
    """

    def __init__(
        self,
        ctx: RenderContext,
        session: Session,
        renderer: RendererService,
        dialogs: DialogService,
        prompts: PromptService,
    ):

        self._ctx = ctx
        self._session = session
        self._renderer = renderer
        self._dialogs = dialogs
        self._prompts = prompts

    async def ask(self, section_key: str, **data) -> str:
        question = await self._renderer.render(self._ctx, section_key, **data)
        return await self._prompts.ask(self._session, question)

    async def ask_secret(self, section_key: str, **data) -> str:
        question = await self._renderer.render(self._ctx, section_key, **data)
        return await self._prompts.ask_secret(self._session, question)

    async def confirm(self, section_key: str, **data) -> bool:
        question = await self._renderer.render(self._ctx, section_key, **data)
        return await self._prompts.confirm(self._session, question)

    async def choice_value(
        self,
        section_key: str,
        options: list[dict],
        *,
        default: str | None = None,
        **data
    ) -> str:
        question = await self._renderer.render(self._ctx, section_key, **data)
        return await self._prompts.choice_value(
            self._session, question, options, default=default, **data
        )

    async def choice_index(self, section_key: str, options: list[str], **data) -> int:
        question = await self._renderer.render(self._ctx, section_key, **data)
        return await self._prompts.choice_index(
            self._session, question, options, **data
        )


class Presenter:
    """
    Handles structured, localized output rendering for a command session.

    Wraps the template context and provides high-level methods for emitting
    messages, failures, and notifications using predefined sections in the template.
    """

    def __init__(
        self,
        template_prefix: str,
        template_key: str,
        session: Session,
        renderer: RendererService,
        dialogs: DialogService,
        prompts: PromptService,
    ) -> RenderContext:
        """
        Constructs a RenderContext based on the current session and template key.

        Args:
            template_prefix (str): the template prefix
            template_key (str): Relative template path (e.g. 'account/cmd_login').
            session: Session object with language information.
            renderer: Renderservice to render the template.

        Returns:
            RenderContext: Template context with full key and language.
        """
        self._prompts = None
        self._session = session
        self._renderer_srv = renderer
        self._dialog_srv = dialogs
        self._prompt_srv = prompts

        self._ctx = RenderContext(
            key=template_key,
            prefix=template_prefix,
            lang=session.lang,
            format=session.output_format,
        )

    @property
    def prompts(self) -> PresenterPrompts:
        if not self._prompts:
            self._prompts = PresenterPrompts(
                self._ctx,
                self._session,
                self._renderer_srv,
                self._dialog_srv,
                self._prompt_srv,
            )
        return self._prompts

    async def emit(self, section: str, **data):
        """
        Renders and emits a section of the current template via session.emit().

        Used for standard informational output (e.g. success, details, confirmations).

        Args:
            section (str): Template section key (e.g. "success", "info").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer_srv.render(self._ctx, section, **data)
        await self._session.emit(text)

    async def fail(self, section: str, **data):
        """
        Renders and sends a failure message via session.fail().

        Used to communicate errors, invalid inputs, or blocked operations.

        Args:
            section (str): Template section key (e.g. "not_found", "denied").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer_srv.render(self._ctx, section, **data)
        await self._session.fail(text)

    async def notify(self, section: str, **data):
        """
        Renders and sends a passive notification via session.notify().

        Used for non-critical messages, hints or background updates.

        Args:
            section (str): Template section key (e.g. "hint", "auto_saved").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer_srv.render(self._ctx, section, **data)
        await self._session.notify(text)


class PresenterService:

    def __init__(self, services: ServiceDirectory):
        self._services = services

    async def create_presenter(
        self, template_prefix: str, template_key: str, session: Session
    ) -> Presenter:

        dialog_service = self._services.get(DialogService)
        render_service = self._services.get(RendererService)
        prompt_service = self._services.get(PromptService)

        return Presenter(
            template_prefix,
            template_key,
            session,
            render_service,
            dialog_service,
            prompt_service,
        )
