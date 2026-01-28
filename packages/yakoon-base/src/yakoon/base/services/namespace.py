
from yakoon.base.controllers.base.directory import BaseControllerDirectory
from yakoon.base.controllers.base.service import ControllerService
from yakoon.base.runtime.session import BaseSession
from yakoon.base.models.namespace import Namespace


class NamespaceService(ControllerService):

    _domain: str = "yakoon"
    
    def __init__(self, domain:str=None):
        self._domain = domain or self._domain
        
    async def from_session(self, session: BaseSession) -> Namespace:
        return Namespace(
            domain=self._domain,    
            bucket="bucket", # session.data_storage.get("realm", "bucket", self._domain), 
            scope="develop"  #session.account_id
        )

    async def get_by_bucket(self, bucket: str="bucket", scope: str="develop") -> Namespace:
        return Namespace(self._domain, bucket, scope)