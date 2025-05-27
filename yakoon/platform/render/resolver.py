from enum import Enum
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from yakoon.platform.render.filters import register_filters
from yakoon.platform.render.render_mode import RenderMode
from yakoon.platform.settings import Settings


ROOT_DIR = Path(__file__).resolve().parents[2]  # geht nach yakoon/
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


def render_template_for(template_key: str, context: dict, mode: RenderMode | None = None) -> str:
    """
    Renders a template from templates/<template_key>/<format>, e.g. cmd_version/js.md
    Fallbacks to js.txt if preferred format not found.
    """
    mode = mode or Settings.runtime.render_mode
    
    preferred = f"{template_key}/j2.{mode.value}"
    fallback = f"{template_key}/j2.plain"

    for name in [preferred, fallback]:
        try:
            tmpl = env.get_template(name)
            return tmpl.render(**context)
        except TemplateNotFound:
            continue

    raise LookupError(f"Template missing: {template_key} ({mode.value})")
