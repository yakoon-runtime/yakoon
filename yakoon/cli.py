import argparse
import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "template"


def init_project(name: str):
    """
    python -m yakoon.cli --init minddojo
    """

    target = Path(name)
    if target.exists():
        print(f"Projektordner '{name}' existiert bereits.")
        return

    shutil.copytree(TEMPLATE_DIR, target)
    print(f"✅ Projekt '{name}' wurde erstellt.")


def main():
    parser = argparse.ArgumentParser(description="Yakoon CLI")
    parser.add_argument("--init", help="Erzeuge ein neues Yakoon-Projekt")

    args = parser.parse_args()

    if args.init:
        init_project(args.init)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
