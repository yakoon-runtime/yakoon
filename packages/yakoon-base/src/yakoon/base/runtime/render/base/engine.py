
from abc import ABC, abstractmethod
from typing import Iterable

from yakoon.base.runtime.render.models.context import RenderContext
from yakoon.base.runtime.render.models.mode import RenderMode
from yakoon.base.runtime.render.models.section import RenderSection
from yakoon.base.runtime.views.template import TemplateSource


class BaseRenderEngine(ABC):
    """
    Abstract base class for all render engines.

    A RenderEngine is responsible for transforming a template section into a formatted string
    based on the given context, rendering mode (e.g. markdown, plain), and content.

    This allows interchangeable output engines (e.g. Jinja, TTS, Markdown, Debug),
    depending on runtime environment, user preferences, or platform capabilities.

    Implementations must define how templates are located, loaded, and rendered.
    """

    @abstractmethod
    async def render(
        self,
        ctx: RenderContext,
        section: RenderSection,
        mode: RenderMode | None = None
    ) -> str:
        pass

    async def build_environment(self, sources: Iterable[TemplateSource]):
        pass
