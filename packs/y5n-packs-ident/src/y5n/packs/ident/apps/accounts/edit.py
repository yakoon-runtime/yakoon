from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    username = req.arg(0)
    changes = {
        "password": req.option("password"),
        "enabled": req.option("enabled"),
        "name": req.option("name"),
        "mail": req.option("mail"),
        "language": req.option("language"),
    }
    changes = {k: v for k, v in changes.items() if v is not None}

    ns_svc = ports.get("ident.namespaces")
    namespace = await ns_svc.account_namespace()

    accounts_svc = ports.get("ident.accounts")
    account = await accounts_svc.edit_account(
        namespace=namespace,
        username=username,
        changes=changes,
    )

    doc = ports.get("document")
    result = await doc.render(
        name="default",
        state={"account": account},
    )
    await io.write(result)
