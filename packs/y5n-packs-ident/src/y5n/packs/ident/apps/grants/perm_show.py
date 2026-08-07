from y5n.sdk import context, io, ports


async def main():
    req = context.request()
    path = req.arg(0)

    ns_svc = ports.get("ident.namespaces")
    permgrant_svc = ports.get("ident.permgrant")

    grants = await permgrant_svc.list_path_grants(
        namespace=await ns_svc.permgrant_namespace(),
        path=path,
    )
    doc = ports.get("document")
    result = await doc.render(name="default", state={"grants": grants, "path": path})
    await io.write(result)
