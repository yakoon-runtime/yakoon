
def translate_ansi(text: str) -> str:
    return (
        text
        .replace("|c", "\x1b[36m")
        .replace("|w", "\x1b[37m")
        .replace("|r", "\x1b[31m")
        .replace("|g", "\x1b[32m")
        .replace("|n", "\x1b[0m")
    )
