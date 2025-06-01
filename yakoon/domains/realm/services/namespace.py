
from yakoon.domains.platform.runtime.session import PlatformSession
from yakoon.domains.realm.models.key.namespace import Namespace


class NamespaceService:

    _domain: str = "realm"
    
    def __init__(self, domain:str=None):
        self._domain = domain or self._domain
        
    async def from_session(self, session: PlatformSession) -> Namespace:
        return Namespace(
            bucket=session.data_storage.get("realm", "bucket", self._domain), 
            owner="system"  #session.account_id
        )
