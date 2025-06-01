
from yakoon.domains.platform.models.account import Account
from yakoon.domains.platform.runtime.session import PlatformSession


async def ensure_admin_account(session: PlatformSession):
    """
    Creates the initial admin account if it does not exist.
    """
    services = session.ctx.gateway.services.get_registry("gateway")
    if await services.accounts.get_by_id("admin") is None:
        admin = Account(
            id="admin",
            name="admin",
            # cmd_groups=["admin", "system"]
            cmd_groups=["realm:system", "realm:account", "realm:character",]
        )
        await services.accounts.save(admin)