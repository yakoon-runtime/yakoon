from collections.abc import Iterable
from pathlib import Path

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    PrefixLoader,
    TemplateNotFound,
)

from yakoon.base.descriptors.template import TemplateSource
from yakoon.platform.runtime.render.base import BaseRenderEngine
from yakoon.platform.runtime.render.context import RenderContext
from yakoon.platform.runtime.render.jinja.filters import register_filters
from yakoon.platform.runtime.render.section import RenderSection
from yakoon.platform.settings import settings


def build_env(
    plugin_sources: Iterable[TemplateSource],
    platform_package: str = "yakoon.platform.bootstrap",  # Beispiel
    platform_templates_path: str = "templates",
    host_override_dir: Path | None = None,
) -> Environment:
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
        src.package: PackageLoader(src.package, src.template_path)
        for src in plugin_sources
        if src
    }
    loaders.append(PrefixLoader(plugin_prefix_map, delimiter=":"))

    # 3) Platform defaults (auch mit Prefix)
    platform_prefix_map = {
        "platform": PackageLoader(platform_package, platform_templates_path)
    }
    loaders.append(PrefixLoader(platform_prefix_map, delimiter=":"))

    env = Environment(
        loader=ChoiceLoader(loaders),
        autoescape=False,  # Markdown, nicht HTML
        trim_blocks=True,
        lstrip_blocks=True,
        enable_async=False,  # rendert sync (tmpl.render). Async optional.
    )

    register_filters(env)  # Filter einmal zentral
    return env


class JinjaEngine(BaseRenderEngine):

    _env = None

    def __init__(self, sources: Iterable[TemplateSource]):
        self._env = build_env(sources)

    async def render(self, ctx: RenderContext, section: RenderSection) -> str:
        """
        Renders a template from templates/<lang>/<key>/<section>.j2.<format>.
        Fallbacks to <section>.j2.plain if preferred format not found.
        """

        fmt = ctx.format or settings.output.format
        # Section key is the filename. No multi-section templates.
        preferred = f"{ctx.prefix}:{ctx.lang}/{ctx.key}/{section.key}.yaml"
        fallback_1 = f"{ctx.prefix}:{ctx.lang}/{ctx.key}/{section.key}.yml"
        fallback_2 = f"{ctx.prefix}:{ctx.lang}/{ctx.key}/{section.key}.json"

        for name in [preferred, fallback_1, fallback_2]:
            try:
                tmpl = self._env.get_template(name)
                # we still pass the section object for convenience (data + key)
                return tmpl.render(section=section)
            except TemplateNotFound:
                continue

        raise LookupError(
            f"Template missing: {ctx.prefix}:{ctx.lang}/{ctx.key}/{section.key} "
            f"(.yaml or .yml or .json)"
        )
