
import subprocess
import os
from pathlib import Path

def run_webclient():

    yakoon_root = Path(__file__).resolve().parents[3]  # geht nach yakoon/
    webclient_dir = yakoon_root / "apps" / "webclient"

    if not (webclient_dir / "package.json").exists():
        print(f"❌ package.json not found in {webclient_dir}")
        return

    print(f"📦 Starting npm in: {webclient_dir}")
    subprocess.run(["npm.cmd", "run", "dev"], cwd=webclient_dir, shell=True)

if __name__ == "__main__":
    run_webclient()
