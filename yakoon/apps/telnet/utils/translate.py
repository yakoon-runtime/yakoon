
def translate_ansi(text: str) -> str:
    return (
        text
        .replace("|c", "\x1b[36m")  # cyan
        .replace("|w", "\x1b[37m")  # white
        .replace("|r", "\x1b[31m")  # red
        .replace("|g", "\x1b[32m")  # green
        .replace("|y", "\x1b[33m")  # yellow
        .replace("|b", "\x1b[34m")  # blue
        .replace("|m", "\x1b[35m")  # magenta
        .replace("|d", "\x1b[90m")  # dark gray
        .replace("|B", "\x1b[1m")   # bold
        .replace("|u", "\x1b[4m")   # underline
        .replace("|h", "\x1b[7m")   # inverse
        .replace("|n", "\x1b[0m")   # reset
    )
