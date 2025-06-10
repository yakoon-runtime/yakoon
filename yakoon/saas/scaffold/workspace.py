import shutil
from pathlib import Path


TEMPLATE_DIR = Path(__file__).parent / "template" 


def scaffold_workspace(app_name: str, target_dir: Path):
    """
    Copy the scaffold template and rewrite imports to match the new app namespace.
    """
    if target_dir.exists():
        raise FileExistsError(f"Target directory '{target_dir}' already exists.")

    shutil.copytree(TEMPLATE_DIR, target_dir)
    rewrite_imports(target_dir, original="yakoon.mesh", replacement=f"{app_name}.runtime")
    print(f"✅ Scaffold '{app_name}' created at {target_dir}")


def rewrite_imports(path: Path, original: str, replacement: str):
    """
    Replace all imports in .py files from `original` to `replacement`.
    """
    for file in path.rglob("*.py"):
        content = file.read_text(encoding="utf-8")
        new_content = content.replace(f"from {original}", f"from {replacement}")
        new_content = new_content.replace(f"import {original}", f"import {replacement}")
        if new_content != content:
            file.write_text(new_content, encoding="utf-8")