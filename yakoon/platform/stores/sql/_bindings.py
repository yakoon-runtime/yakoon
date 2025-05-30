from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService
from yakoon.platform.stores._db.sqlite import SessionLocal
from yakoon.platform.stores.sql.account import SQLAccountStore
from yakoon.platform.stores.sql.session import SQLSessionStore


def bind_sql_storages():
    """
    Binds all services to SQLite-backed SQLAlchemy stores.
    Used for development or lightweight persistence scenarios.
    """
    db = SessionLocal()
    
    SessionService.bind_storage(SQLSessionStore(db))
    AccountService.bind_storage(SQLAccountStore(db))
