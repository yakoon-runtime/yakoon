import shlex

class Request:

    def __init__(self, raw: str):
        self._raw = raw.strip()

        if not self._raw:
            self._command = ""
            self._args = []
            return

        parts = shlex.split(self._raw, posix=True)

        self._command = parts[0].lower()
        self._args = parts[1:]

    @property
    def raw(self) -> list[str]:
        """
        Returns the original input string.

        This value is immutable and must not be modified.
        All parsing operations derive from this value.
        """
        return self._raw

    def command(self) -> str:
        """Returns the command name (first token)."""
        return self._command

    def args(self) -> list[str]:
        """Returns all arguments as a list of tokens."""

    def arg(self, index: int, default=None):
        try:
            return self._args[index]
        except IndexError:
            return default
        
    def rest(self) -> str:
        parts = self._raw.split(maxsplit=1)
        return parts[1] if len(parts) == 2 else ""        
        
    def has_args(self) -> bool:
        return bool(self._args)

    def arg_count(self) -> int:
        return len(self._args)
    
    def split_commands(self, separator: str = ";") -> list[str]:
        """
        Splits a raw command string into individual commands.

        - Trims whitespace
        - Removes empty segments
        - Does not handle quoting or escaping (by design)
        """
        return [p.strip() for p in self._raw.split(separator) if p.strip()]
