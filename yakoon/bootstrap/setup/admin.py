
from yakoon.domains.gateway.models.account import Account
from yakoon.domains.gateway.services.account import AccountService


async def ensure_admin_account(accounts: AccountService):
    """
    Creates the initial admin account if it does not exist.
    """
    if await accounts.get_by_id("admin") is None:
        admin = Account(
            id="admin",
            name="admin",
            # cmd_groups=["admin", "system"]
            cmd_groups=["realm:system", "realm:account", "realm:character",]
        )
        await accounts.save(admin)