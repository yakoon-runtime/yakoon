
from yakoon.platform.runtime.session import PlatformSession
from yakoon.domains.realm.models.key.namespace import Namespace

class NamespaceService:

    @staticmethod
    async def from_session(session: PlatformSession) -> Namespace:
        return Namespace(
            bucket=session.data_storage.get("realm", "bucket", "realm"), 
            owner="system"  #session.account_id
        )
