import asyncio


async def safe_input(prompt: str = "$ ") -> str:
    """
    Asynchronously reads user input from stdin without creating extra closures or tasks.

    This function avoids memory growth issues associated with standard ainput()
    by offloading input() to a thread executor.

    Args:
        prompt (str): Optional prompt to display.

    Returns:
        str: The entered user input.
    """
    print(prompt, end="", flush=True)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input)
