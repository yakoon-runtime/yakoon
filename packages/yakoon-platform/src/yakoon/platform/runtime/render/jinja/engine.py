from pathlib import Path
from typing import Iterable, Optional

from yakoon.base.runtime.views.template import TemplateSource

from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.context import RenderContext
from yakoon.platform.runtime.render.mode import RenderMode
from yakoon.platform.runtime.render.section import RenderSection
from yakoon.platform.runtime.render.base import BaseRenderEngine
from yakoon.platform.runtime.render.jinja.filters import register_filters


from jinja2 import (
    Environment,
    ChoiceLoader,
    FileSystemLoader,
    PackageLoader,
    PrefixLoader,
    TemplateNotFound,
)

def build_env(
    plugin_sources: Iterable[TemplateSource],
    platform_package: str = "yakoon.platform.bootstrap",   # Beispiel
    platform_templates_path: str = "templates",
    host_override_dir: Optional[Path] = None) -> Environment:
    """
    Reihenfolge ist wichtig:
      1) Host overrides (filesystem) – ganz vorne
      2) Plugin templates (per Prefix)
      3) Platform default templates (per Prefix)
    """

    loaders = []

    # 1) Host overrides (optional) – z.B. /etc/yakoon/templates
    if host_override_dir:
        # Hier erwarten wir Pfade wie: <override>/<prefix>/<lang>/<key>/j2.markdown
        loaders.append(FileSystemLoader(str(host_override_dir)))

    # 2) Plugin-Loader: PrefixLoader mappt prefix -> PackageLoader
    plugin_prefix_map = {
        src.name: PackageLoader(src.package, src.package_path)
        for src in plugin_sources if src
    }
    loaders.append(PrefixLoader(plugin_prefix_map, delimiter=":"))

    # 3) Platform defaults (auch mit Prefix)
    platform_prefix_map = {
        "platform": PackageLoader(platform_package, platform_templates_path)
    }
    loaders.append(PrefixLoader(platform_prefix_map, delimiter=":"))

    env = Environment(
        loader=ChoiceLoader(loaders),
        autoescape=False,     # Markdown, nicht HTML
        trim_blocks=True,
        lstrip_blocks=True,
        enable_async=False,   # rendert sync (tmpl.render). Async optional.
    )

    register_filters(env)     # Filter einmal zentral
    return env


class JinjaEngine(BaseRenderEngine):

    _env = None

    def __init__(self, sources: Iterable[TemplateSource]):
        self._env = build_env(sources)

    #  def render_template(env: Environment, prefix: str, lang: str, key: str, mode: str, section) -> str:
    # out = render_template(env, "office.mailing", "de", "mail_send", "markdown", section)

    #async def render(self, env: Environment, prefix: str, ctx: RenderContext, section: RenderSection, mode: RenderMode | None = None) -> str:
    async def render(self, ctx: RenderContext, section: RenderSection, mode: RenderMode | None = None) -> str:
        """
        Renders a template from templates/<template_key>/<format>, e.g. cmd_version/js.md
        Fallbacks to js.txt if preferred format not found.
        """
        
        ctx.prefix = "yakoon.platform"

        mode = mode or settings.render.render_mode
        preferred = f"{ctx.prefix}:{ctx.lang}/{ctx.key}/j2.{mode.value}"
        fallback = f"{ctx.prefix}:{ctx.lang}/{ctx.key}/j2.plain"

        for name in [preferred, fallback]:
            try:
                tmpl = self._env.get_template(name)
                return tmpl.render(section=section)
            except TemplateNotFound:
                continue

        raise LookupError(f"Template missing: {ctx.lang}/{ctx.key} ({mode.value})")
