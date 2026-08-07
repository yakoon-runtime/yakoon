from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    accountname = req.arg(0)

    ns_svc = ports.get("ident.namespaces")
    accounts_svc = ports.get("ident.accounts")
    joins_svc = ports.get("ident.joins")

    account = await accounts_svc.get_by_username(
        namespace=await ns_svc.account_namespace(),
        username=accountname,
    )
    if not account:
        await io.write(f"Account '{accountname}' not found.")
        return

    joins = await joins_svc.list_account_joins(
        namespace=await ns_svc.join_namespace(),
        account_key=account.key,
    )

    doc = ports.get("document")
    result = await doc.render(
        name="default", state={"joins": joins, "account": accountname}
    )
    await io.write(result)
