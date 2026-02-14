from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.runtime.session import Session
from yakoon.platform.runtime.render.context import RenderContext


class PresenterPrompts:

    DEFAULT_POLICY = "system:string"
    DEFAULT_SECRET_POLICY = "system:secret"

    def __init__(self, ctx, session: Session, services: ServiceDirectory):
        self._ctx = ctx
        self._session = session
        self._prompts = services.get(ports.PromptService)
        self._policy = services.get(ports.PolicyService)
        self._renderfields = services.get(ports.FieldSpecRenderService)

    async def ask(
        self, section_key: str, *, policy: str = DEFAULT_POLICY, **data
    ) -> str:
        field = await self._renderfields.build(
            self._ctx,
            section_key=section_key,
            policy=policy,
            **data,
        )
        while True:
            raw = await self._prompts.ask(self._session, field)
            res = self._policy.validate_field(field=field, raw=raw)
            if res.ok:
                return res.value

            # simplest error output; later: render template section "invalid_input"
            for err in res.errors:
                await self._session.emit(f"[{err.field_key}] {err.message}")

    async def ask_secret(
        self, section_key: str, *, policy: str = DEFAULT_SECRET_POLICY, **data
    ) -> str:
        return await self.ask(section_key, policy=policy, **data)

    async def confirm(
        self, section_key: str, *, policy: str = DEFAULT_POLICY, **data
    ) -> bool:
        field = await self._renderfields.build(
            self._ctx,
            section_key=section_key,
            policy=policy,
            **data,
        )
        return await self._prompts.confirm(self._session, field)

    async def choice_value(
        self,
        section_key: str,
        *,
        policy: str = DEFAULT_POLICY,
        options: list[dict],
        default: str | None = None,
        **data,
    ) -> str:
        field = await self._renderfields.build(
            self._ctx,
            section_key=section_key,
            policy=policy,
            **data,
        )
        return await self._prompts.choice_value(
            self._session, field, options, default=default
        )

    async def choice_index(
        self,
        section_key: str,
        *,
        policy: str = DEFAULT_POLICY,
        options: list[str],
        **data,
    ) -> int:
        field = await self._renderfields.build(
            self._ctx,
            section_key=section_key,
            policy=policy,
            **data,
        )
        return await self._prompts.choice_index(
            self._session,
            field,
            options,
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
        services: ServiceDirectory,
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
        self._services = services
        self.renderer = self._services.get(ports.RendererService)

        self._ctx = RenderContext(
            key=template_key,
            prefix=template_prefix,
            lang=session.lang,
            format=session.output_format,
        )

    @property
    def prompts(self) -> PresenterPrompts:
        if not self._prompts:
            self._prompts = PresenterPrompts(self._ctx, self._session, self._services)
        return self._prompts

    async def emit(self, section: str, **data):
        """
        Renders and emits a section of the current template via session.emit().

        Used for standard informational output (e.g. success, details, confirmations).

        Args:
            section (str): Template section key (e.g. "success", "info").
            **data: Optional key-value pairs for template variables.
        """
        text = await self.renderer.render(self._ctx, section, **data)
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

        return Presenter(
            template_prefix,
            template_key,
            session,
            self._services,
        )
