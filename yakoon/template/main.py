import asyncio
from yakoon.apps.console.app import run_application
from yakoon.game.definition import GameDefinition


if __name__ == "__main__":
    asyncio.run(run_application(GameDefinition))