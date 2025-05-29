

from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.settings import Settings
from yakoon.engine.system.session import BaseSession


async def ask(session: BaseSession, prompt_text: str) -> str:
    """     
    Asks the user for free-text input based on a rendered template section.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        str: The user's input as a string.
    """
    await session.emit(prompt_text)
    return await DialogManager.set_prompt(session, Settings.prompt_timed_out)


async def confirm(session: BaseSession, prompt_text: str) -> bool:
    """
    Asks the user for a yes/no confirmation using a template-based prompt.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    while True:
        answer = await ask(f"{prompt_text} (y/n)")
        if answer.lower() in ("y", "yes", "j", "ja"):
            return True
        if answer.lower() in ("n", "no", "nein"):
            return False
        await session.emit("Bitte antworte mit 'y' oder 'n'.")


async def choice(session: BaseSession, prompt_text: str, options: list[str]) -> str:
    """
    Presents the user with a list of choices and returns the selected value.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        str: The chosen value.
    """
    options_str = ", ".join(options)
    while True:
        answer = await ask(f"{prompt_text} ({options_str})")
        if answer in options:
            return answer
        await session.emit(f"Bitte wähle eine der Optionen: {options_str}")


async def choice_index(session: BaseSession, prompt_text: str, options: list[str]) -> str:
    """
    Presents the user with a numbered list of choices and returns the selected index.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        int: The index of the selected choice (starting at 0).
    """
    if not options:
        raise ValueError("choice() requires at least one option.")

    # Ausgabe der nummerierten Liste
    msg = [prompt_text]
    for idx, opt in enumerate(options, 1):
        msg.append(f"[{idx}] {opt}")
    await session.emit("\n".join(msg))

    # Dialogschleife
    while True:
        answer = await ask("Nummer eingeben:")
        if answer.isdigit():
            index = int(answer) - 1
            if 0 <= index < len(options):
                return index, options[index]
        await session.emit("Bitte eine gültige Nummer eingeben.")