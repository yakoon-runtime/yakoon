import asyncio
from yakoon.loop.loop import start_loop
from yakoon.loop.controllers.directory import AppControllerDirectory


if __name__ == "__main__":
    asyncio.run(start_loop(AppControllerDirectory()))