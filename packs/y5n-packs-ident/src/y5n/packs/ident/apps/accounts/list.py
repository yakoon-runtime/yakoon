from y5n.sdk import io, ports


async def main():
    ns_svc = ports.get("ident.namespaces")
    namespace = await ns_svc.account_namespace()

    accounts_svc = ports.get("ident.accounts")
    accounts = await accounts_svc.list_accounts(namespace=namespace)

    doc = ports.get("document")
    result = await doc.render(
        name="default",
        state={"accounts": accounts},
    )
    await io.write(result)
