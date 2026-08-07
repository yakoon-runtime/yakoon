from y5n.sdk import context, io, ports, security


async def main():
    req = context.request()
    username = req.arg(0)
    secret = req.option("password")

    if req.has_option("administrative"):
        security_context = security.SecurityContext.ADMINISTRATIVE
    elif req.has_option("temporary"):
        security_context = security.SecurityContext.TEMPORARY
    else:
        security_context = security.SecurityContext.NORMAL

    auth = ports.get("ident.auth")
    result = await auth.authenticate(
        username=username,
        secret=secret,
        security_context=security_context,
    )

    state = {"user": username, "reason": None}
    if result.get("ok") and result.get("user"):
        state["user"] = result["user"].get("username", username)
    else:
        state["reason"] = result.get("reason")

    doc = ports.get("document")
    projection = await doc.render(
        name="default",
        state=state,
    )
    await io.write(projection)
