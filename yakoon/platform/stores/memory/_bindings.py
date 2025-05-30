from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService
from yakoon.platform.stores.memory.account import InMemoryAccountStore
from yakoon.platform.stores.memory.session import InMemorySessionStore

def bind_memory_storages():

    SessionService.bind_storage(InMemorySessionStore())
    AccountService.bind_storage(InMemoryAccountStore())
