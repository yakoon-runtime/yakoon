
from yakoon.engine.services.session import BaseSessionService
from yakoon.platform.services.session import SessionService
from yakoon.platform.stores.memory.session import InMemorySessionStore
from yakoon.solution.platform.runtime.session import SolutionSession


class SolutionSessionService(SessionService):
    """
    SessionService implementation specific to the current solution.

    You can override methods, customize session lifecycle,
    or switch to a different session store backend here.
    """
    
    def __init__(self, store: BaseSessionService = None):
        self.store = store or InMemorySessionStore(session_cls=SolutionSession)
