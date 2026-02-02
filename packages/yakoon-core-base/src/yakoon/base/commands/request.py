import shlex

class Request:

    def __init__(self, raw: str):
        self.raw = raw.strip()

        if not self.raw:
            self.cmd = ""
            self.args = []
            return

        parts = shlex.split(self.raw, posix=True)

        self.cmd = parts[0].lower()
        self.args = parts[1:]

    def get_arg(self, index: int, default=None):
        try:
            return self.args[index]
        except IndexError:
            return default
        
    def get_rest(self) -> str:
        parts = self.raw.split(maxsplit=1)
        return parts[1] if len(parts) == 2 else ""        
        
    def has_args(self) -> bool:
        return bool(self.args)

    def arg_count(self) -> int:
        return len(self.args)