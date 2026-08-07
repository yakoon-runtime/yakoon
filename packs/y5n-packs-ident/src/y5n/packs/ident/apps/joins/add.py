from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    accountname = req.arg(0)
    groupname = req.arg(1)

    ns_svc = ports.get("ident.namespaces")
    accounts_svc = ports.get("ident.accounts")
    groups_svc = ports.get("ident.groups")
    joins_svc = ports.get("ident.joins")

    account = await accounts_svc.get_by_username(
        namespace=await ns_svc.account_namespace(),
        username=accountname,
    )
    if not account:
        await io.write(f"Account '{accountname}' not found.")
        return

    group = await groups_svc.get_by_name(
        namespace=await ns_svc.group_namespace(),
        name=groupname,
    )
    if not group:
        await io.write(f"Group '{groupname}' not found.")
        return

    join_obj = await joins_svc.add_join(
        namespace=await ns_svc.join_namespace(),
        account_key=account.key,
        group_key=group.key,
    )

    doc = ports.get("document")
    result = await doc.render(name="default", state={"join": join_obj})
    await io.write(result)
