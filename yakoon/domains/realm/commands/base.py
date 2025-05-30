
from yakoon.domains.realm.models.key.namespace import Namespace
from yakoon.domains.realm.services.namespace import NamespaceService
from yakoon.engine.core.command import Command
from yakoon.platform.render.context import Presenter


class RealmCommand(Command):

    async def get_template_path(self) -> str:
        return f"domains/realm/commands/{self.template_key}"
    
    async def get_presenter(self, session) -> Presenter:
        return Presenter(await self.get_template_path(), session)
    
    async def get_namespace(self, session) -> Namespace:
        return await NamespaceService.from_session(session)
