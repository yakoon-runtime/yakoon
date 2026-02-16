from dataclasses import asdict

from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.runtime.session import Session
from yakoon.platform.runtime.render.context import RenderContext


class PresenterPrompts:

    def __init__(
        self, ctx: RenderContext, session: Session, services: ServiceDirectory
    ):
        self._ctx = ctx
        self._session = session
        self._renderfields = services.get(ports.FieldSpecRenderService)
        self._inputs = services.get(ports.InputService)

    async def ask(
        self,
        section_key: str,
        *,
        policy: str = ports.PresenterPrompts.DEFAULT_POLICY,
        **data,
    ) -> object:
        field = await self._renderfields.build(
            self._ctx,
            section_key=section_key,
            policy=policy,
            **data,
        )
        return await self._inputs.ask_field(self._session, field)

    async def ask_secret(
        self,
        section_key: str,
        *,
        policy: str = ports.PresenterPrompts.DEFAULT_MASK_POLICY,
        **data,
    ) -> object:
        return await self.ask(section_key, policy=policy, **data)


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
        self._renderer = self._services.get(ports.RendererService)

        self._ctx = RenderContext(
            key=template_key,
            prefix=template_prefix,
            lang=session.lang,
        )

    @property
    def prompts(self) -> PresenterPrompts:
        if not self._prompts:
            self._prompts = PresenterPrompts(self._ctx, self._session, self._services)
        return self._prompts

    async def emit(self, section: str, **data) -> None:
        spec = await self._renderer.render_spec(self._ctx, section, **data)
        await self._session.emit(asdict(spec))

    async def fail(self, section: str, **data) -> None:
        spec = await self._renderer.render_spec(self._ctx, section, **data)
        await self._session.fail(asdict(spec))

    async def notify(self, section: str, **data) -> None:
        spec = await self._renderer.render_spec(self._ctx, section, **data)
        await self._session.notify(asdict(spec))


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
