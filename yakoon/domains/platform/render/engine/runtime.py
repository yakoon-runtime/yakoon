from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from yakoon.domains.platform.render.engine.context import RenderContext
from yakoon.domains.platform.render.engine.filters import register_filters
from yakoon.domains.platform.render.engine.mode import RenderMode
from yakoon.domains.platform.render.engine.section import RenderSection
from yakoon.domains.platform.settings import Settings


ROOT_DIR = Path(__file__).resolve().parents[4]  # geht nach yakoon/
TEMPLATE_DIR = ROOT_DIR / "solution" / "templates"
if not (TEMPLATE_DIR).exists():
    raise ValueError(f"Template directory found: {TEMPLATE_DIR}")
    

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=False, # wir wollen Markdown, nicht HTML escapen
    trim_blocks=True,
    lstrip_blocks=True
)

register_filters(env)


def render_template_for(ctx: RenderContext, section: RenderSection, mode: RenderMode | None = None) -> str:
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
