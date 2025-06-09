from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from yakoon.saas.controllers.gateway.settings import Settings
from yakoon.saas.engines.render.base.engine import BaseRenderEngine
from yakoon.saas.engines.render.jinja.filters import register_filters
from yakoon.saas.engines.render.models.context import RenderContext
from yakoon.saas.engines.render.models.mode import RenderMode
from yakoon.saas.engines.render.models.section import RenderSection


ROOT_DIR = Path(__file__).resolve().parents[3]  # geht nach yakoon/
TEMPLATE_DIR = ROOT_DIR / "bootstrap" / "templates"
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
        mode = mode or Settings.runtime.render_mode
        
        preferred = f"{ctx.lang}/{ctx.key}/j2.{mode.value}"
        fallback = f"{ctx.lang}/{ctx.key}/j2.plain"

        for name in [preferred, fallback]:
            try:
                tmpl = env.get_template(name)
                return tmpl.render(section=section)
            except TemplateNotFound:
                continue

        raise LookupError(f"Template missing: {ctx.lang}/{ctx.key} ({mode.value})")
