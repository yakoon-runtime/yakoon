import asyncio
from yakoon.apps.console.app import run_console
from yakoon.loop.loop import start_loop

from yakoon.loop.controllers.directory import AppControllerDirectory

ready = asyncio.Event()

async def run_console_server():
    ready.set()
    await run_console()

async def main():
    asyncio.create_task(run_console_server())
    await ready.wait()
    await asyncio.sleep(2)
    await start_loop(AppControllerDirectory())


if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.run(start_loop(AppControllerDirectory()))