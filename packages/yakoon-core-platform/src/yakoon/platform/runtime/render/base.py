from abc import ABC, abstractmethod

from yakoon.platform.runtime.render.context import RenderContext
from yakoon.platform.runtime.render.section import RenderSection


class BaseRenderEngine(ABC):
    """
    Abstract base class for all render engines.

    A RenderEngine is responsible for transforming a template section into a
    formatted string based on the given context, rendering mode
    (e.g. markdown, plain), and content.

    This allows interchangeable output engines (e.g. Jinja, TTS, Markdown, Debug),
    depending on runtime environment, user preferences, or platform capabilities.

    Implementations must define how templates are located, loaded, and rendered.
    """

    @abstractmethod
    async def render(self, ctx: RenderContext, section: RenderSection) -> str:
        pass
