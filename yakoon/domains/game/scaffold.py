from pathlib import Path
import shutil
from importlib.resources import path


def create_project(target: Path, name: str):
    from yakoon.domains.game import _scaffold

    if target.exists():
        raise FileExistsError(f"Pfad {target} existiert bereits.")

    with path(_scaffold, "") as src:
        shutil.copytree(src, target)

    print(f"[SCAFFOLD] Projekt '{name}' wurde erstellt unter {target}")