import asyncio
from yakoon.apps.console.app import run_application
from .game.definition import GameController


if __name__ == "__main__":
    asyncio.run(run_application(GameController))