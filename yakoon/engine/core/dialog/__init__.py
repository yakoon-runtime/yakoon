

from yakoon.engine.core.dialog.manager import DialogManager


async def ask(session, prompt_text: str) -> str:
    await session.out(prompt_text)
    return await DialogManager.set_prompt(session)


async def confirm(session, prompt_text: str) -> bool:
    while True:
        answer = await ask(session, f"{prompt_text} (y/n)")
        if answer.lower() in ("y", "yes", "j", "ja"):
            return True
        if answer.lower() in ("n", "no", "nein"):
            return False
        await session.out("Bitte antworte mit 'y' oder 'n'.")


async def choice(session, prompt_text: str, options: list[str]) -> str:
    options_str = ", ".join(options)
    while True:
        answer = await ask(session, f"{prompt_text} ({options_str})")
        if answer in options:
            return answer
        await session.out(f"Bitte wähle eine der Optionen: {options_str}")


async def choice_index(session, prompt_text: str, options: list[str]) -> str:
    if not options:
        raise ValueError("choice() requires at least one option.")

    # Ausgabe der nummerierten Liste
    msg = [prompt_text]
    for idx, opt in enumerate(options, 1):
        msg.append(f"[{idx}] {opt}")
    await session.out("\n".join(msg))

    # Dialogschleife
    while True:
        answer = await ask(session, "Nummer eingeben:")
        if answer.isdigit():
            index = int(answer) - 1
            if 0 <= index < len(options):
                return index, options[index]
        await session.out("Bitte eine gültige Nummer eingeben.")