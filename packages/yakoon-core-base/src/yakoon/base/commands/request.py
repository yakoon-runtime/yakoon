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
        return self._args

    def arg(self, index: int, default=None):
        args = self._pos_args()
        try:
            return args[index]
        except IndexError:
            return default

    def free_text(self) -> str:
        parts = self._raw.split(maxsplit=1)
        return parts[1].lstrip() if len(parts) == 2 else ""

    def option(self, name: str, default=None):
        key = f"--{name}"
        try:
            idx = self._args.index(key)
        except ValueError:
            return default

        if idx + 1 >= len(self._args):
            return default

        value = self._args[idx + 1]
        if value.startswith("--"):
            return default

        return value

    def token(self, index: int, default=None):
        try:
            return self._args[index]
        except IndexError:
            return default

    def has_option(self, name: str) -> bool:
        return f"--{name}" in self._args

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

    def _pos_args(self) -> list[str]:
        """
        Returns positional args only, skipping:
          --flag value
          --flag (no value)
        """
        out: list[str] = []
        i = 0
        while i < len(self._args):
            tok = self._args[i]
            if tok.startswith("--"):
                i += 1
                if i < len(self._args) and not self._args[i].startswith("--"):
                    i += 1
                continue
            out.append(tok)
            i += 1

        return out
