"""err — project the current invocation's error payload.

The engine routes an uncaught exception to a new invocation on this
command (ADR: an error creates a new invocation). The command is an
ordinary node: it reads the error payload from the context and decides
itself how to render it — which template, which language, whether to
audit or log. The engine knows none of this.
"""

from __future__ import annotations

from y5n.sdk import context, ports, runtime

ERROR_NODE = "/usr/bin/err"

# Error type name → resource variant. This mapping is the command's
# Fachlichkeit; the engine only knows the payload, never the variants.
_VARIANTS = {
    "PermissionDenied": "denied",
    "ElevationRequired": "elevation",
    "NodeNotFound": "not_found",
    "NodeNotExecutable": "not_executable",
    "UsageError": "usage",
    "UnknownOptionsError": "unknown_options",
}


async def main():
    err = context.error()

    if err is None:
        await runtime.io.write("Internal Error")
        return

    variant = _VARIANTS.get(err.get("type", ""), "default")

    try:
        resource = await runtime.resolve(
            node_path=ERROR_NODE,
            capability="error",
            parameters={"variant": variant},
        )
    except LookupError:
        await runtime.io.write("Internal Error")
        return

    template = resource.read_text()

    jinja = ports.get("jinja")
    rendered = await jinja(content=template, context={"state": err})

    compile_port = ports.get("compile")
    projection = await compile_port(text=rendered, context={})

    await runtime.io.write(projection)


__all__ = ["main"]
