
from yakoon.mesh.settings import settings
from yakoon.mesh.runtime.render.base.engine import BaseRenderEngine
from yakoon.mesh.runtime.render.models.context import RenderContext
from yakoon.mesh.runtime.render.models.mode import RenderMode
from yakoon.mesh.runtime.render.models.section import RenderSection


class RendererService:

    def __init__(self, engine: BaseRenderEngine, default_mode: RenderMode | None = None):
        self._mode = default_mode or settings.render.render_mode
        self._engine = engine

    async def render(self, ctx: RenderContext, key: str, **data) -> str:
        """
        Renders a specific section of a command template with optional data.

        This is a shorthand for passing a RenderSection object manually,
        useful for compact calls when the section is known.

        Args:
            ctx (RenderContext): The context specifying template path and language.
            key (str): The section key to render (e.g. 'success', 'error').
            **data: Optional keyword arguments passed to the template.

        Returns:
            str: The rendered template section output.
        """    
        section = RenderSection(key, data)
        return await self._engine.render(ctx, section)

    async def render_by_key(self, template_key: str, section: str, lang: str = "de", **data) -> str:
        """
        Renders a section of a template using the current render mode and context.

        Args:
            template_key: logical name of the template (e.g. 'cmd_login')
            section: section name (e.g. 'error', 'success')
            lang: language folder (default: 'de')
            **data: variables passed into the section context

        Returns:
            Rendered string (Markdown, plain text, etc.)
        """
        ctx = RenderContext(key=template_key, lang=lang)
        return await self.render(ctx, section, data)
