from __future__ import annotations

import importlib.resources as ir
from collections.abc import Iterable
from dataclasses import dataclass

from yakoon.base.descriptors.template import TemplateSource
from yakoon.platform.runtime.render.context import RenderContext


@dataclass(slots=True)
class TemplateLoader:

    sources: list[TemplateSource]
    platform_package: str = ""
    platform_templates_path: str = "templates"

    def __init__(self, sources: list[TemplateSource]):
        self.sources = sources

    async def load(self, ctx: RenderContext) -> str:
        """
        Lookup order:
          1) host overrides (filesystem)
          2) plugin sources (TemplateSource)
          3) platform defaults
        """
        exts = (".yaml", ".yml", ".json")

        for src in self._sources_for_prefix(ctx.prefix):
            base = ir.files(src.package)
            rel = self._rel_path(src, ctx)
            for ext in exts:
                candidate = base.joinpath(rel + ext)
                try:
                    if candidate.is_file():
                        return candidate.read_text(encoding="utf-8")
                except FileNotFoundError:
                    pass

        raise LookupError(
            f"Template missing: {ctx.prefix}:{ctx.lang}/{ctx.key} (.yaml or .yml or .json)"
        )

    def _sources_for_prefix(self, prefix: str) -> Iterable[TemplateSource]:
        # in derselben Reihenfolge wie bisher ChoiceLoader-Priority
        for s in self.sources:
            if s and s.package == prefix:
                yield s

    def _rel_path(self, src: TemplateSource, ctx: RenderContext) -> str:
        # src.template_sub_path ist optional (z.B. "core", "system", ...)
        parts = [src.template_path, ctx.lang]
        # if src.template_sub_path:
        #    parts.append(src.template_sub_path.strip("/")) # TODO: Check.
        parts.append(ctx.key)
        return "/".join(parts)
