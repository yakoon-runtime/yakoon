from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    username = req.arg(0)
    password = req.option("password")

    ns_svc = ports.get("ident.namespaces")
    namespace = await ns_svc.account_namespace()

    accounts_svc = ports.get("ident.accounts")
    account = await accounts_svc.add_account(
        namespace=namespace,
        username=username,
        password=password,
        name=req.option("name"),
        mail=req.option("mail"),
        language=req.option("language"),
    )

    doc = ports.get("document")
    result = await doc.render(
        name="default",
        state={"account": account},
    )
    await io.write(result)
