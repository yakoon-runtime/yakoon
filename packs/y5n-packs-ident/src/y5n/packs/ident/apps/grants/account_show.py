from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    accountname = req.arg(0)

    ns_svc = ports.get("ident.namespaces")
    accounts_svc = ports.get("ident.accounts")
    permgrant_svc = ports.get("ident.permgrant")

    account = await accounts_svc.get_by_username(
        namespace=await ns_svc.account_namespace(), username=accountname
    )
    if not account:
        await io.write(f"Account '{accountname}' does not exist.")
        return

    grants = await permgrant_svc.list_subject_grants(
        namespace=await ns_svc.permgrant_namespace(),
        subject_key=account.key,
    )
    doc = ports.get("document")
    result = await doc.render(
        name="default", state={"grants": grants, "subject": accountname}
    )
    await io.write(result)
