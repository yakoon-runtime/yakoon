from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    accountname = req.arg(0)
    path = req.arg(1)

    ns_svc = ports.get("ident.namespaces")
    accounts_svc = ports.get("ident.accounts")
    permgrant_svc = ports.get("ident.permgrant")

    account = await accounts_svc.get_by_username(
        namespace=await ns_svc.account_namespace(), username=accountname
    )
    if not account:
        await io.write(f"Account '{accountname}' does not exist.")
        return

    grant = await permgrant_svc.remove_grant(
        namespace=await ns_svc.permgrant_namespace(),
        subject_key=account.key,
        path=path,
    )
    doc = ports.get("document")
    result = await doc.render(name="default", state={"grant": grant})
    await io.write(result)
