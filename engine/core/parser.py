
class Request:
    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.cmd = ""
        self.subcmd = ""
        self.switches = []
        self.args = []
        self.kwargs = {}

        parts = self.raw.split()

        # Command + optional subcommand
        if parts:
            self.cmd = parts[0].lower()
        if len(parts) > 1 and not parts[1].startswith(("/", "--")):
            self.subcmd = parts[1].lower()

        # Parse remaining parts
        for part in parts[2:]:
            if part.startswith("/"):
                self.switches.append(part[1:])
            elif "=" in part:
                key, val = part.split("=", 1)
                self.kwargs[key.lower()] = val
            else:
                self.args.append(part)

    def is_match(self, *patterns: str) -> bool:
        """
        example:
          if request.is_match("item drop", "item delete"):
        """
        return f"{self.cmd} {self.subcmd}".strip() in patterns                

    def get_arg(self, index: int, default=None, cast=str):
        try:
            return cast(self.args[index])
        except (IndexError, ValueError):
            return default

    def get_kwarg(self, key: str, default=None, cast=str):
        """
        example:
          request.get_kw("speed", 5, int)
        """
        val = self.kwargs.get(key.lower(), default)
        try:
            return cast(val) if val is not None else default
        except Exception:
            return default

    def has_switch(self, name: str) -> bool:
        return name.lower() in self.switches


def request_to_debug_dict(req: Request) -> dict:
    return {
        "cmd": req.cmd,
        "subcmd": req.subcmd,
        "switches": req.switches,
        "args": req.args,
        "kwargs": req.kwargs,
        "raw": req.raw,
    }