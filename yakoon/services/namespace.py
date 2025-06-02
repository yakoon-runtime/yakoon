
from yakoon.domains.gateway.runtime.session import GatewaySession
from yakoon.models.namespace import Namespace


class NamespaceService:

    _domain: str = "yakoon"
    
    def __init__(self, domain:str=None):
        self._domain = domain or self._domain
        
    async def from_session(self, session: GatewaySession) -> Namespace:
        return Namespace(
            domain=self._domain,    
            bucket="bucket", # session.data_storage.get("realm", "bucket", self._domain), 
            scope="develop"  #session.account_id
        )
