from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.message import MessageSpec
from yakoon.platform.runtime.render.base import BaseRenderEngine
from yakoon.platform.runtime.render.context import RenderContext
from yakoon.platform.runtime.render.section import RenderSection


class RendererService:

    def __init__(self, services: ServiceDirectory, engine: BaseRenderEngine):
        self._services = services
        self._engine = engine

    async def render_text(self, ctx: RenderContext, key: str, **data) -> str:
        section = RenderSection(key, data)
        return await self._engine.render(ctx, section)

    async def render_spec(self, ctx: RenderContext, key: str, **data) -> MessageSpec:
        yaml_text = await self.render_text(ctx, key, **data)
        messages = self._services.get(ports.MessageSpecService)
        return await messages.parse_spec(yaml_text)
