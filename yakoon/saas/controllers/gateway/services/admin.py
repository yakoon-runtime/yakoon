
from yakoon.mesh.models.key import Key
from yakoon.saas.controllers.gateway.models.account import Account
from yakoon.saas.controllers.gateway.services.account import AccountService


async def ensure_admin_account(accounts: AccountService):
    """
    Creates the initial admin account if it does not exist.
    """
    admin_key = Key.from_parts("yakoon", "system", "system", "admin")
    if await accounts.get_by_key(admin_key) is None:
        admin = Account(admin_key, name="Admin",
            permissions=["system"],
            cmd_groups=["admin", "system", "realm:system", "realm:account", "realm:character",]
        )
        await accounts.save(admin)

    #TODO: Nur für unsere Tests.
    stefan_key = Key.from_parts("yakoon", "bucket", "develop", "stefan")
    if await accounts.get_by_key(stefan_key) is None:
        user = Account(stefan_key, name="Stefan",
            permissions=["system"],
            cmd_groups=["admin", "system", "realm:system", "realm:account", "realm:character",]
        )
        await accounts.save(user)