
from yakoon.saas.commands.command import SaasCommand
from yakoon.saas.domains.realm.services.registry import RealmServiceRegistry


class RealmCommand(SaasCommand):

    async def get_template_path(self) -> str:
        return f"domains/realm/commands/{self.template_key}"
    
    async def get_domain_services(self) -> RealmServiceRegistry:
        return await super().get_domain_services()
