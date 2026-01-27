from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from yakoon.base.runtime.render.base.engine import BaseRenderEngine
from yakoon.base.runtime.render.jinja.filters import register_filters
from yakoon.base.runtime.render.models.context import RenderContext
from yakoon.base.runtime.render.models.mode import RenderMode
from yakoon.base.runtime.render.models.section import RenderSection
from yakoon.base.settings import settings


ROOT_DIR = Path(__file__).resolve().parents[4]  # geht nach yakoon/ vorher 3
TEMPLATE_DIR = ROOT_DIR / "platform" / "bootstrap" / "templates"
if not (TEMPLATE_DIR).exists():
    raise ValueError(f"Template directory found: {TEMPLATE_DIR}")
    

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=False, # wir wollen Markdown, nicht HTML escapen
    trim_blocks=True,
    lstrip_blocks=True
)

register_filters(env)


class JinjaEngine(BaseRenderEngine):

    async def render(self, ctx: RenderContext, section: RenderSection, mode: RenderMode | None = None) -> str:
        """
        Renders a template from templates/<template_key>/<format>, e.g. cmd_version/js.md
        Fallbacks to js.txt if preferred format not found.
        """
        
        mode = mode or settings.render.render_mode
        preferred = f"{ctx.lang}/{ctx.key}/j2.{mode.value}"
        fallback = f"{ctx.lang}/{ctx.key}/j2.plain"

        for name in [preferred, fallback]:
            try:
                tmpl = env.get_template(name)
                return tmpl.render(section=section)
            except TemplateNotFound:
                continue

        raise LookupError(f"Template missing: {ctx.lang}/{ctx.key} ({mode.value})")
