import re
from typing import Any


_NAMED_ARG_RE = re.compile(r"(?P<flag>--[a-zA-Z0-9][\w\-]*)\s+(?P<ph>\{\{[^}]+\}\})")
_PLACEHOLDER_RE = re.compile(r"\{\{\s*([^}]+?)\s*\}\}")


def compile_run_command(cmd: str, values: dict[str, Any], *, context: str) -> str:
    out = cmd

    # 1) Named args: --flag {{key}}
    def repl_named(m: re.Match) -> str:
        flag = m.group("flag")
        ph = m.group("ph")
        key = ph[2:-2].strip()
        val = values.get(key)

        if val is None or val == "":
            return ""  # optional: remove whole --flag <value>

        return f"{flag} {val}"

    out = _NAMED_ARG_RE.sub(repl_named, out)

    # 2) Replace remaining placeholders ONLY if value exists and is not None/""
    for k, v in values.items():
        if v is None or v == "":
            continue
        out = out.replace("{{" + k + "}}", str(v))

    # normalize whitespace
    out = " ".join(out.split())

    # 3) Guardrail: after rendering there must be no unresolved placeholders left
    m = _PLACEHOLDER_RE.search(out)
    if m:
        raise ValueError(
            f"{context}: unresolved placeholder '{{{{{m.group(1)}}}}}' in: {out}"
        )

    return out

