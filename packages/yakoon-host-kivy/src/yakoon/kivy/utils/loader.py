from __future__ import annotations
from pathlib import Path
from kivy.lang import Builder


def _sorted_kv(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        (p for p in folder.rglob("*.kv") if p.is_file()),
        key=lambda p: p.as_posix(),
    )

def load_layouts(package_root: Path) -> None:
    layouts = package_root / "layouts"

    # 0) theme/base widgets first
    theme_kv = layouts / "theme.kv"
    if theme_kv.exists():
        Builder.load_file(str(theme_kv))

    # 1) widgets
    for kv in _sorted_kv(layouts / "widgets"):
        Builder.load_file(str(kv))

    # 2) pages
    for kv in _sorted_kv(layouts / "pages"):
        Builder.load_file(str(kv))

    # 3) app root
    app_kv = layouts / "app.kv"
    if app_kv.exists():
        Builder.load_file(str(app_kv))