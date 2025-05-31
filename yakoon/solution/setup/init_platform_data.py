
from yakoon.domains.platform.models.account import Account
from yakoon.domains.platform.services.account import AccountService


async def ensure_admin_account():
    """
    Creates the initial admin account if it does not exist.
    """
    if await AccountService.get_by_id("admin") is None:
        admin = Account(
            id="admin",
            name="admin",
            # cmd_groups=["admin", "system"]
            cmd_groups=["realm:system", "realm:account", "realm:character",]
        )
        await AccountService.save(admin)